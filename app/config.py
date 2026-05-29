import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
    NEBIUS_API_KEY = os.getenv("NEBIUS_API_KEY")
    NEBIUS_BASE_URL = os.getenv("NEBIUS_BASE_URL")
    NEBIUS_MODEL = os.getenv("NEBIUS_MODEL")
    APP_ENV = os.getenv("APP_ENV", "development")
