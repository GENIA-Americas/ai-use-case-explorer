# ai-use-case-explorer

Part of the GENIA Americas AI Toolkit — repo #3. Reference library of AI use cases,
matched to readiness/maturity results.

## Setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

## Run
```bash
uvicorn app.main:app --reload
```
Docs at http://127.0.0.1:8000/docs

## Test
```bash
pytest tests/ -v
```
8/8 tests pass as of last verified run.

## Auth
Reads are open (`GET /use-cases`, `GET /use-cases/{id}`) — this is a shared reference
library other tools in the toolkit consult freely, so browsing/searching it needs no key.
Writes (`POST /use-cases`, `DELETE /use-cases/{id}`) require an `X-Admin-Key` header,
configured via the `ADMIN_API_KEYS` env var as a comma-separated list of valid keys —
otherwise any anonymous caller on the public internet could pollute or wipe this library.

## API
- `POST /use-cases` — add a use case (title, industry, category, complexity, tags).
  Requires `X-Admin-Key`.
- `GET /use-cases` — list, filterable by `industry`, `category`, `complexity`. Open.
- `GET /use-cases/{id}` — retrieve one. Open.
- `DELETE /use-cases/{id}` — remove one. Requires `X-Admin-Key`.
- `GET /health`
