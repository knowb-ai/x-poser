# Contributing to X-Poser Mini

Thanks for your interest in contributing. X-Poser Mini is a small workshop/demo project for checking a claim from X against retrieved web evidence and rendering a compact report.

The goal of this repo is to keep the smoke-test path clear, understandable, and easy to run locally.

## Development Setup

1. Clone the repo.
2. Create and activate a Python virtual environment.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Configure environment variables from `.env.example`.
5. Start the app:

```bash
uvicorn app.main:app --reload
```

6. Open `http://127.0.0.1:8000`.

Required environment variables:

- `TAVILY_API_KEY`
- `NEBIUS_API_KEY`
- `NEBIUS_BASE_URL`

Optional environment variables:

- `NEBIUS_MODEL`
- `APP_ENV`

## Pull Requests

1. Create a branch from `main`.
2. Keep the change small and focused.
3. Update documentation when setup, environment variables, endpoints, or user-facing behavior changes.
4. Run the app locally and test the changed path manually.
5. Open a PR against `main` using the most relevant PR template.

One concern per PR. Avoid bundling unrelated cleanup with feature or bug-fix work.

## Project Scope

This release is intentionally minimal:

- Paste a claim from X.
- Retrieve web evidence with Tavily.
- Judge the claim with a Nebius-backed LLM through the OpenAI-compatible SDK.
- Display a compact evidence-linked report.

Out of scope for this repo right now:

- Automatic monitoring or posting to X.
- n8n workflow integration.
- Production-scale scheduling, queues, persistence, or moderation workflows.

If a proposed change expands the project beyond the smoke-test path, describe the tradeoff clearly in the PR.

## Code Style

- Prefer small, direct modules over broad abstractions.
- Keep route handlers, service clients, schemas, and rendering concerns separated according to the existing `app/` layout.
- Use explicit environment configuration through `app/config.py`.
- Keep user-facing errors understandable and safe to display.
- Avoid adding dependencies unless they are necessary for the demo path.

## Verification

This repo does not currently define a formal test suite or lint command. Until that changes, contributors should at minimum:

- Start the app with `uvicorn app.main:app --reload`.
- Check `GET /api/health`.
- Submit a representative claim through the UI.
- Confirm the report includes a verdict, confidence, summary, evidence links, and share text.
- Confirm missing API keys produce a clear health or runtime failure.

If you add automated tests or linting, include the commands in `README.md` and update this guide.

## Agentic Contributors

Codex and other code agents are welcome collaborators on this project. If you are contributing as a code agent, follow these rules on top of everything above:

- Keep edits tightly scoped to the requested change.
- Do not add dependencies without a clear reason.
- Do not introduce unrelated refactors.
- Do not commit secrets or real `.env` values.
- Prefer ASCII in code, comments, and docs.
- Avoid placeholder TODO comments in submitted code.
- Preserve the workshop/demo nature of the project.

## Reporting Issues

When reporting a bug, include:

- What claim or input was used.
- Whether API keys were configured.
- The observed behavior.
- The expected behavior.
- Any relevant server output with secrets removed.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
