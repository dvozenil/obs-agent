from fastapi import FastAPI, HTTPException, status
import httpx, time

app = FastAPI()

@app.get("/health")
async def health():
    return {"status": "ok"} 

@app.get("/check")
async def check(url: str):
    start = time.monotonic()
    try:
        async with httpx.AsyncClient() as client:
            headers = {"User-Agent": "obs-agent/0.1"}
            response = await client.get(url, headers=headers, timeout=10.0, follow_redirects=True)
    except httpx.RequestError as exc:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(exc))
    end = time.monotonic()
    elapsed = end - start
    return {"status_code": response.status_code, "redirected": bool(response.history), "original_url": url,
             "final_url": str(response.url), "latency_seconds": elapsed}