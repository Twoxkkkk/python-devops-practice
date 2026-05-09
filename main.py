from uvicorn import run
from fastapi import FastAPI, Body
from datetime import datetime, timezone
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Counter

app = FastAPI(title="DevOps Practice App")

Instrumentator().instrument(app).expose(app, endpoint="/metrics")

echo_requests = Counter("echo_requests_total", "Total POST /echo requests")

@app.get("/")
def root():
    return {"message": "Hello, DevOps!"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/echo")
async def echo(data: dict = Body(...)):
    echo_requests.inc()

    data["timestamp"] = datetime.now(timezone.utc).isoformat()
    return data
    

if __name__ == "__main__":
    run(app, host="0.0.0.0", port=8000)


