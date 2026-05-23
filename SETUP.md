# SnipURL — setup & how to use in the masterclass

A tiny, **fully runnable** FastAPI URL shortener used as the demo repo. It ships with **no real docs and 3 planted bugs** so the doc-generation, code-review, and debugging demos have genuine work to do.

## Files
```
snipurl/
├── main.py            # FastAPI app: POST /shorten, GET /{code}, GET /stats/{code}
├── service.py         # base62 encode + shorten()  (2 planted bugs)
├── storage.py         # in-memory store            (1 planted bug)
├── models.py          # Pydantic request/response models
├── tests/test_snipurl.py  # 1 passing test + 2 xfail tests that document the bugs
├── requirements.txt
├── README.md          # deliberately bare — the doc demo expands this
└── .gitignore
```

## The 3 planted bugs (for your debugging/review demos)
1. **`storage.py` → `increment_clicks`** computes `count + 1` but never stores it, so clicks stay 0.
2. **`service.py` → `encode_base62(0)`** returns `""` instead of a valid code (zero edge case).
3. **`service.py` → `record_visit(code, log=[])`** uses a mutable default argument shared across calls.
   *(Bonus: `main.py` redirect returns no 404 for unknown codes.)*

The two `xfail` tests in `tests/` make this visible: `pytest` is green today, and when a demo **fixes** a bug, its test flips from `xfail` → `pass` — a satisfying live "green checkmark" moment.

## Run it locally
```bash
python -m venv .venv && source .venv/bin/activate   # optional
pip install -r requirements.txt
pytest -q                       # -> 1 passed, 2 xfailed
uvicorn main:app --reload       # then open http://127.0.0.1:8000/docs
```
Quick manual check:
```bash
curl -X POST http://127.0.0.1:8000/shorten -H "Content-Type: application/json" -d '{"url":"https://anthropic.com"}'
curl http://127.0.0.1:8000/stats/b
```
*(All of the above was verified before class — the app boots, endpoints respond, and `/docs` Swagger loads.)*

## Push it to GitHub (so the runbook's `git clone` works)
The repo is already initialized with one commit. To publish:
```bash
# with the GitHub CLI:
gh repo create snipurl --public --source=. --push

# or manually:
git remote add origin https://github.com/<you>/snipurl.git
git branch -M main
git push -u origin main
```
Then in the runbook, Step 1 becomes:
```bash
git clone https://github.com/<you>/snipurl.git
```

## Tip for the doc-generation demo
Because `README.md` is intentionally one line, asking Claude Code to "write a proper README" produces an obvious, dramatic before/after. Same for the missing `docs/` — let Claude create `docs/architecture.md` (Mermaid) and `docs/api.md` from scratch.
