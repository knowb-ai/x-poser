from fastapi import FastAPI

from app.routes.api import router as api_router
from app.routes.pages import router as pages_router

app = FastAPI(title="X-Poser Mini")

app.include_router(api_router)
app.include_router(pages_router)
