# X-Poser Mini
X-Poser Mini is a small workshop/demo project for a claim-checking smoke test.
Public story for this release:
"Paste a claim from X, retrieve web evidence with Tavily, judge it with a Nebius-backed LLM, and display a compact evidence-linked report."

## Release scope
- Minimal open-source smoke path only.
- No automatic monitoring or posting to X.
- No n8n workflow integration in this release.

## How it works
1. User submits claim text (with optional tweet URL).
2. App runs web retrieval with Tavily.
3. App sends stitched evidence to a Nebius-hosted model (OpenAI-compatible API).
4. App renders a compact report with verdict, confidence, summary, evidence links, and share text.

## External dependencies
- Tavily: web search and evidence retrieval.
- Nebius AI Studio: model inference endpoint.

This repo uses the `openai` Python SDK against Nebius' OpenAI-compatible `base_url`.

## Quickstart
1. Create and activate a virtual environment.
2. Install dependencies:
   - `pip install -r requirements.txt`
3. Configure `.env` from `.env.example`.
4. Start the app:
   - `uvicorn app.main:app --reload`
5. Open `http://127.0.0.1:8000`.

## Environment variables
Required:
- `TAVILY_API_KEY`
- `NEBIUS_API_KEY`
- `NEBIUS_BASE_URL`

Optional:
- `NEBIUS_MODEL`
- `APP_ENV` (default: `development`)

## Endpoints
- `GET /` — demo UI
- `POST /api/check` — full smoke-test pipeline
- `GET /api/health` — key-availability health check

## Notes
- This project is intentionally small and workshop-oriented.
- The current flow is designed for smoke testing and demo reliability, not production-scale operations.

## License
MIT
