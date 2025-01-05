import redis.asyncio as redis

from contextlib import asynccontextmanager

from decouple import config
from fastapi import FastAPI, HTTPException, Depends
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from pydantic import BaseModel

import helpers

REDIS_URL = config("REDIS_URL")

@asynccontextmanager
async def lifespan(_:FastAPI):
    redis_conn = redis.from_url(REDIS_URL)
    await FastAPILimiter.init(redis_conn)
    yield
    await redis_conn.close()

app = FastAPI(lifespan=lifespan)

      

@app.get("/", dependencies=[Depends(RateLimiter(times=1, seconds=5))])
def read_index():
    return {"Hello": "World"}


class ImageGenerationRequest(BaseModel):
    prompt: str


@app.post("/generate", dependencies=[Depends(RateLimiter(times=1, seconds=5))])
def generate_image(data: ImageGenerationRequest):
    try:
        pred_result = helpers.generate_image(data.prompt)
        return pred_result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))