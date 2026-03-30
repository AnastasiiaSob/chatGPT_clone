## Cursor Instructions

Follow tasks sequentially.
Do not modify unrelated files.
Ask before changing database schema.

# Task
In this project, you'll build a full-stack AI chat application with WebSocket communication, streaming responses, and multi-modal capabilities. You'll implement real-time message streaming, image analysis with OpenAI's Vision API, and advanced state management with React reducers, perfect for demonstrating modern asynchronous architecture.

## Why behind it

This project proves you understand real-time communication, streaming data, and AI integration while gaining hands-on experience with FastAPI WebSockets, OpenAI APIs, React useReducer, TypeScript, and async Python patterns. Key features include streaming chat responses, image upload/analysis, sentiment tracking, markdown rendering, and connection state management.

# Requirements

## Pre-step
[X] Create the project structure and add all needed dependencies

## Step 1: Backend WebSocket Implementation

 - [X] Create a simple WebSocket endpoint using FastAPI that accepts user inputs (start from src/routes/v1/endpoints.py)
 - [X] For each user input, generate a response using ChatGPT
 - [X] Send the generated response back to the client over the WebSocket
 - [X] Implement proper error handling and connection management
 - [X] Create tests to check the implemented functionality

## Step 2: Chat Interface Implementation

- [ ] Create a responsive chat UI with a clean and modern design
- [ ] Implement a main chat panel where user and AI messages are displayed
- [ ] Add input controls for users to submit messages
- [ ] Connect to the WebSocket endpoint to send user inputs and receive AI responses
- [ ] Display AI responses in real-time as they arrive from the backend 

## Step 3: Response Visualization

- [ ] Display AI response with appropriate styling to distinguish it from user messages
- [ ] Implement a simple visualization component to show basic metrics about the response (e.g., response time, length, sentiment)
- [ ] Allow users to provide feedback on AI responses (thumbs up/down)

## Step 4: Bonus Tasks

- [ ] Implement response streaming from OpenAI API to the frontend through WebSockets
- [ ] Add a typing effect visualization for streaming responses
- [ ] Implement image upload functionality allowing users to send images to the chat
- [ ] Enable OpenAI's vision capabilities to analyze and respond to uploaded images
- [ ] Add responsive design for mobile and tablet devices
- [ ] Add tests for Backend

# Use this project structure
chatgpt_clone/
│
├── BE/                                   # Backend (FastAPI + Python)
│   ├── src/
│   │   ├── routes/                       # API route handlers (empty starter)
│   │   ├── helpers/                      # Helper functions (empty starter)
│   │   ├── utils/                        # Utility modules (empty starter)
│   │   ├── main.py                       # FastAPI application entry point
│   │   └── settings.py                   # Configuration & environment variables
│   ├── .env                              # Environment variables (API keys)
│   ├── Dockerfile                        # Backend container configuration
│   └── requirements.txt                  # Python dependencies
│
├── FE/                                   # Frontend (Next.js + React + TypeScript)
│   ├── src/
│   │   └── app/
│   │       ├── chat/                     # Chat feature folder (empty starter)
│   │       ├── globals.css               # Global styles
│   │       ├── layout.tsx                # Root layout component
│   │       └── page.tsx                  # Home page
│   ├── Dockerfile                        # Frontend container configuration
│   ├── package.json                      # Node.js dependencies
│   └── next.config.ts                    # Next.js configuration
│
├── docker-compose.yaml                   # Orchestrates both containers
├── PLAN.md                               # Setup instructions
└── README.md                             # Project documentation
