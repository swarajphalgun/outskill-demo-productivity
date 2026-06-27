# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

**SnipURL** — a tiny FastAPI URL shortener used as a live masterclass demo repo. It is intentionally minimal and ships with **3 planted bugs** plus deliberately bare docs so that doc-generation, code-review, and debugging demos have real work to do. See [SETUP.md](SETUP.md) for the full demo framing.

## Commands

```bash
pip install -r requirements.txt
pytest -q                       # expect: 1 passed, 2 xfailed
pytest tests/test_snipurl.py::test_shorten_creates_code   # run a single test
uvicorn main:app --reload       # serve; Swagger UI at http://127.0.0.1:8000/docs
```

There is no build step, linter, or formatter configured.

## Architecture

A three-layer flow, one module per layer, no framework beyond FastAPI/Pydantic:

- [main.py](main.py) — FastAPI app and the three routes: `POST /shorten`, `GET /{code}` (redirect), `GET /stats/{code}`. Owns the single module-level `store = Storage()` instance.
- [service.py](service.py) — pure logic: `encode_base62` (id → code) and `shorten(storage, url)` which allocates an id, encodes it, and saves. Codes are assigned sequentially (`next_id` → base62), so the first shortened URL is always code `b` (id 1).
- [storage.py](storage.py) — in-memory `Storage` (two dicts + a counter). No persistence; restarting the server clears all data.
- [models.py](models.py) — Pydantic request/response models.

`GET /{code}` is a catch-all route, so it shadows any path not matched earlier — keep new specific routes (like `/stats/{code}`) declared with their own prefixes.

## The planted bugs (important)

These are **intentional** and are the subject of the demos — do not silently "clean them up" unless the task is explicitly to fix them:

1. `storage.py` → `increment_clicks` computes `count + 1` but discards it; clicks stay 0.
2. `service.py` → `encode_base62(0)` returns `""` instead of a valid code.
3. `service.py` → `record_visit(code, log=[])` uses a shared mutable default argument.
4. (Bonus) `main.py` redirect does not 404 on an unknown code (`long_url` is `None`).

The two `@pytest.mark.xfail(strict=True)` tests in [tests/test_snipurl.py](tests/test_snipurl.py) document bugs #1 and #2. Because they are `strict`, **fixing a bug flips its test from `xfail` to a failing run unless you also remove the `xfail` marker** — when fixing, delete the corresponding marker so the test reports as a normal pass.
