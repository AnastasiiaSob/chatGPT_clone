"use client";

import React, { useEffect, useMemo, useReducer, useRef } from "react";
import styles from "./chat.module.css";

type Role = "user" | "assistant" | "error";

type ChatMessage = {
  id: string;
  role: Role;
  content: string;
};

type ConnectionState = "connecting" | "connected" | "disconnected" | "error";

type State = {
  messages: ChatMessage[];
  connection: ConnectionState;
  input: string;
  isGenerating: boolean;
  errorBanner: string | null;
};

type WsEvent =
  | { type: "status"; message: string }
  | { type: "user_message_received"; message: string }
  | { type: "ai_response"; message: string }
  | { type: "error"; message: string }
  | { type: string; message?: string };

type Action =
  | { type: "ws_status"; connection: ConnectionState }
  | { type: "set_input"; value: string }
  | { type: "send_request" }
  | { type: "user_message_received"; message: string }
  | { type: "ai_response"; message: string }
  | { type: "ws_error"; message: string };

function uid(): string {
  // Generates a unique id for rendering list items.
  if (typeof crypto !== "undefined" && "randomUUID" in crypto) return crypto.randomUUID();
  return `${Date.now()}-${Math.random().toString(16).slice(2)}`;
}

function parseWsEvent(raw: string): WsEvent | null {
  // Parses backend WebSocket JSON messages; returns null on invalid payload.
  try {
    const data = JSON.parse(raw) as WsEvent;
    if (!data || typeof data !== "object" || !("type" in data)) return null;
    return data;
  } catch {
    return null;
  }
}

function chatReducer(state: State, action: Action): State {
  // Updates chat state based on WebSocket events / UI actions.
  switch (action.type) {
    case "ws_status": {
      return {
        ...state,
        connection: action.connection,
      };
    }
    case "set_input": {
      return { ...state, input: action.value };
    }
    case "send_request": {
      return { ...state, isGenerating: true, errorBanner: null };
    }
    case "user_message_received": {
      return {
        ...state,
        messages: [
          ...state.messages,
          { id: uid(), role: "user", content: action.message },
        ],
      };
    }
    case "ai_response": {
      return {
        ...state,
        isGenerating: false,
        messages: [
          ...state.messages,
          { id: uid(), role: "assistant", content: action.message },
        ],
      };
    }
    case "ws_error": {
      return {
        ...state,
        isGenerating: false,
        errorBanner: action.message,
        messages: [
          ...state.messages,
          { id: uid(), role: "error", content: action.message },
        ],
      };
    }
    default:
      return state;
  }
}

export default function ChatPage() {
  const initialState: State = useMemo(
    () => ({
      messages: [],
      connection: "connecting",
      input: "",
      isGenerating: false,
      errorBanner: null,
    }),
    [],
  );

  const [state, dispatch] = useReducer(chatReducer, initialState);
  const wsRef = useRef<WebSocket | null>(null);
  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  const wsUrl =
    process.env.NEXT_PUBLIC_WS_URL ?? "ws://localhost:8000/api/v1/ws";

  useEffect(() => {
    // Establishes a WebSocket connection and dispatches actions based on messages.
    const ws = new WebSocket(wsUrl);
    wsRef.current = ws;

    dispatch({ type: "ws_status", connection: "connecting" });

    ws.onopen = () => {
      dispatch({ type: "ws_status", connection: "connected" });
    };

    ws.onmessage = (event) => {
      const evt = parseWsEvent(String(event.data));
      if (!evt) return;

      switch (evt.type) {
        case "status":
          // The backend sends a connected status event right after accept().
          dispatch({ type: "ws_status", connection: "connected" });
          return;
        case "user_message_received":
          dispatch({
            type: "user_message_received",
            message: evt.message ?? "",
          });
          return;
        case "ai_response":
          dispatch({
            type: "ai_response",
            message: evt.message ?? "",
          });
          return;
        case "error":
          dispatch({ type: "ws_error", message: evt.message ?? "Unknown error" });
          return;
        default:
          return;
      }
    };

    ws.onerror = () => {
      dispatch({
        type: "ws_error",
        message: "WebSocket error.",
      });
    };

    ws.onclose = () => {
      dispatch({ type: "ws_status", connection: "disconnected" });
    };

    return () => {
      ws.close();
    };
  }, [wsUrl]);

  useEffect(() => {
    // Keeps the conversation scrolled to the newest message.
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth", block: "end" });
  }, [state.messages.length]);

  function handleInputChange(value: string) {
    // Updates the controlled input in reducer state.
    dispatch({ type: "set_input", value });
  }

  function handleSubmit(e: React.FormEvent) {
    // Sends the current input as `{message: string}` over WebSocket.
    e.preventDefault();
    const text = state.input.trim();
    if (!text) return;

    const ws = wsRef.current;
    if (!ws || ws.readyState !== WebSocket.OPEN) {
      dispatch({ type: "ws_error", message: "Not connected to the server." });
      return;
    }

    ws.send(JSON.stringify({ message: text }));
    dispatch({ type: "send_request" });
    dispatch({ type: "set_input", value: "" });
  }

  const canSend = state.connection === "connected" && state.input.trim().length > 0;

  return (
    <main className={styles.page}>
      <div className={styles.header}>
        <div className={styles.titleBlock}>
          <h1 className={styles.title}>Chat</h1>
          <div className={styles.subTitle}>
            Connection: <span className={styles.badge}>{state.connection}</span>
          </div>
        </div>

        {state.errorBanner ? (
          <div className={styles.errorBanner}>{state.errorBanner}</div>
        ) : null}
      </div>

      <section className={styles.chatShell}>
        <div className={styles.messages} aria-live="polite">
          {state.messages.map((m) => (
            <div
              key={m.id}
              className={[
                styles.bubble,
                m.role === "user" ? styles.bubbleUser : "",
                m.role === "assistant" ? styles.bubbleAssistant : "",
                m.role === "error" ? styles.bubbleError : "",
              ].join(" ")}
            >
              {m.content}
            </div>
          ))}

          {state.isGenerating ? (
            <div className={[styles.bubble, styles.bubbleAssistant].join(" ")}>
              AI is thinking...
            </div>
          ) : null}

          <div ref={messagesEndRef} />
        </div>

        <form className={styles.composer} onSubmit={handleSubmit}>
          <input
            className={styles.input}
            value={state.input}
            onChange={(e) => handleInputChange(e.target.value)}
            placeholder="Type a message..."
            disabled={state.connection !== "connected"}
          />
          <button className={styles.button} type="submit" disabled={!canSend}>
            Send
          </button>
        </form>
      </section>
    </main>
  );
}

