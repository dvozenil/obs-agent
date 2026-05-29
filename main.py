from fastapi import FastAPI, HTTPException, status, Request
import httpx, time
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.http = httpx.AsyncClient(
        headers = {"User-Agent": "obs-agent/0.1"},
        timeout=10.0,
        follow_redirects=True
    )
    yield
    await app.state.http.aclose()

app = FastAPI(lifespan=lifespan)

@app.get("/health")
async def health():
    return {"status": "ok"} 

@app.get("/check")
async def check(request: Request, url: str):
    start = time.monotonic()
    try:
        client = request.app.state.http
        response = await client.get(url)
    except httpx.RequestError as exc:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(exc))
    end = time.monotonic()
    elapsed = end - start
    return {"status_code": response.status_code, "redirected": bool(response.history), "original_url": url,
             "final_url": str(response.url), "latency_seconds": elapsed}