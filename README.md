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
5/5 tests pass as of last verified run.

## API
- `POST /use-cases` — add a use case (title, industry, category, complexity, tags).
- `GET /use-cases` — list, filterable by `industry`, `category`, `complexity`.
- `GET /use-cases/{id}` — retrieve one.
- `DELETE /use-cases/{id}` — remove one.
- `GET /health`
