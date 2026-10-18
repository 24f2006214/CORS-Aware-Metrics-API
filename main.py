import time
import uuid

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse


EMAIL = "24f2006214@ds.study.iitm.ac.in"
ALLOWED_ORIGIN = "https://dash-bu0120.example.com"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.middleware("http")
async def required_headers(request, call_next):
    started = time.perf_counter()
    response = await call_next(request)
    elapsed = time.perf_counter() - started
    response.headers["X-Request-ID"] = str(uuid.uuid4())
    response.headers["X-Process-Time"] = f"{elapsed:.6f}"
    return response


@app.get("/stats")
async def stats(values: str = Query(...)):
    try:
        numbers = [int(item.strip()) for item in values.split(",")]
    except ValueError:
        return JSONResponse(
            status_code=400,
            content={"detail": "values must be comma-separated integers"},
        )

    if not numbers:
        return JSONResponse(status_code=400, content={"detail": "values cannot be empty"})

    total = sum(numbers)
    return {
        "email": EMAIL,
        "count": len(numbers),
        "sum": total,
        "min": min(numbers),
        "max": max(numbers),
        "mean": total / len(numbers),
    }

