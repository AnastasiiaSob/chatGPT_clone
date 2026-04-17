export default function HomePage() {
  return (
    <main className="container">
      <div className="card">
        <h1>ChatGPT Clone</h1>
        <p>
          Go to the chat page:{" "}
          <a href="/chat" style={{ textDecoration: "underline" }}>
            /chat
          </a>
        </p>
      </div>
    </main>
  );
}

