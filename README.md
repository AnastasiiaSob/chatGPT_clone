## ChatGPT Clone (Full-stack)

### Structure

- `BE/`: FastAPI backend (WebSocket + OpenAI integration will be added in Step 1+)
- `FE/`: Next.js frontend (chat UI will be added in Step 2+)

### Local dev (no Docker)

Backend:

```bash
cd BE
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn src.main:app --reload --port 8000
```

Frontend:

```bash
cd FE
npm install
npm run dev
```

### Docker dev

```bash
cp BE/.env.example BE/.env
docker compose up --build
```

