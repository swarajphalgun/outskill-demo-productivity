from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from models import ShortenRequest, ShortenResponse, StatsResponse
from storage import Storage
from service import shorten, record_visit

app = FastAPI(title="SnipURL", version="0.1.0")
store = Storage()


@app.post("/shorten", response_model=ShortenResponse)
def create_short_url(req: ShortenRequest):
    code = shorten(store, req.url)  # NOTE: no validation that req.url is a real URL
    return ShortenResponse(code=code, short_url=f"http://snip.url/{code}")


@app.get("/{code}")
def redirect_to_url(code: str):
    long_url = store.get_url(code)
    store.increment_clicks(code)
    record_visit(code)
    return RedirectResponse(long_url)  # BUG: unknown code -> long_url is None; should return 404


@app.get("/stats/{code}", response_model=StatsResponse)
def get_stats(code: str):
    return StatsResponse(
        code=code,
        long_url=store.get_url(code),
        clicks=store.get_clicks(code),
    )
