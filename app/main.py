from fastapi import FastAPI
from app.twitter_client import monitor_targets

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    await monitor_targets()
