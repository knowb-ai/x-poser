import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
    TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
    TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
    TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
    TWITTER_ACCESS_SECRET = os.getenv("TWITTER_ACCESS_SECRET")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    # X-Poser Mini smoke test
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
    NEBIUS_API_KEY = os.getenv("NEBIUS_API_KEY")
    NEBIUS_BASE_URL = os.getenv("NEBIUS_BASE_URL")
    NEBIUS_MODEL = os.getenv("NEBIUS_MODEL")
    APP_ENV = os.getenv("APP_ENV", "development")
