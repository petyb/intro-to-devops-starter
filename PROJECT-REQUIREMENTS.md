# Project requirements — Intro to DevOps course app

This document describes what your application should do. When you fork this repo, keep it updated with these requirements.

---

## Project layout

- **Application code** lives in a subfolder **`app/`**. Put your API handlers, data model, and business logic there. The root of the repo is for config, docs, and entrypoints (e.g. `main.go` or `main.py` that starts the server and imports from `app`).
- Use a clear structure inside `app/` (e.g. `app/handlers`, `app/models`, `app/store`) so that unit and integration tests can target specific parts.

---

## What the application is

A **simple REST API** that manages a single resource — **fruits** (a small catalog). It must:

- Expose a **health endpoint** (for load balancers and health checks).
- Stay **small** so the focus is on DevOps practices, not application code.

---

## Functional requirements

| # | Requirement |
|---|-------------|
| 1 | **Health check** — `GET /health` (or `/ready`) returns 200 and a simple status (e.g. `{"status": "ok"}`). |
| 2 | **List** — `GET /fruits` returns all fruits (JSON array). Optional query params (e.g. `?in_season=true`, `?limit=10`) if you want. |
| 3 | **Create** — `POST /fruits` accepts a JSON body (e.g. `name`, `price`, `in_season`), creates a fruit, returns it with an `id`. |
| 4 | **Get one** — `GET /fruits/{id}` returns a single fruit or 404. |
| 5 | **Update** — `PUT /fruits/{id}` updates a fruit; returns updated fruit or 404. |
| 6 | **Delete** — `DELETE /fruits/{id}` deletes a fruit; returns 204 or 404. |

**Data model:** One resource is enough: e.g. `id`, `name`, `price`, `in_season`, (optional) `created_at`. No authentication in the app.

---

## Tests

- **Unit tests** — Test one unit of behavior in isolation (e.g. a function that computes something, or a handler with a fake store). They should be fast and not start the real server or hit the network. Use them to verify logic, edge cases, and error handling.
- **Integration tests** — Test that parts work together (e.g. HTTP client → real server → in-memory store). They may start the app or a test server and send real requests. Use them to verify that endpoints behave correctly end-to-end (status codes, JSON shape, 404 when missing).

You must have both: unit tests for core logic and integration tests for the API. Put unit tests next to the code they test (e.g. `app/handlers/handlers_test.go`) or in an `app/.../test` package; put integration tests in a dedicated folder (e.g. `tests/` or `integration/`) so they are easy to run separately if needed.

---

Stick to these requirements; you can use AI to help implement them, but you must understand what the code does.
