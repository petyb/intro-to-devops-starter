# FruitAPI

Coursework fork of [intro-to-devops-starter](https://github.com/AntonAleksandrov13/intro-to-devops-starter).
A small REST API for managing fruits — the canvas for working through the
DevOps practices in the course (CI, Docker, IaC, AWS, observability, CD).

Spec: [PROJECT-REQUIREMENTS.md](./PROJECT-REQUIREMENTS.md).

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET    | `/health`            | liveness — `{"status":"ok"}` |
| GET    | `/fruits`            | list all fruits; `?in_season=true|false` filters |
| GET    | `/fruits/cheapest`   | fruit with the lowest price (404 if none) |
| GET    | `/fruits/{id}`       | one fruit or 404 |
| POST   | `/fruits`            | create (`name`, `price`, `in_season`) → 201 |
| PUT    | `/fruits/{id}`       | partial update or 404 |
| DELETE | `/fruits/{id}`       | delete → 204 or 404 |

## Local development

```bash
python3.13 -m venv .venv
.venv/bin/pip install -r requirements-dev.txt
.venv/bin/uvicorn app.main:app --reload
```

Tests:

```bash
.venv/bin/pytest tests/test_main.py             # unit
FRUITAPI_BASE_URL=http://127.0.0.1:8000 \
  .venv/bin/pytest tests/test_integration.py    # integration (needs running server)
```

## Docker

```bash
docker build -t fruitapi:dev .
docker run --rm -p 8000:8000 fruitapi:dev
```

Multi-stage build on `python:3.13-slim-bookworm`, non-root user, healthcheck.

## Branching strategy

**Trunk-based.** Short-lived feature branches off `main`, opened as PRs.
`main` is the only long-lived branch and is the source of truth for releases.

- PRs run unit tests (`.github/workflows/pr.yml`) and must be green to merge.
- Merges to `main` run the full pipeline (`.github/workflows/main.yml`):
  unit tests → build image → integration tests → push to GHCR → SBOM.
