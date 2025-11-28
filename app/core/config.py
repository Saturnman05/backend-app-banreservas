from dotenv import load_dotenv
import os

load_dotenv()

DEV = "development"


class Settings:
    DEV = "development"
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", DEV)


ENV = os.getenv("ENVIRONMENT", DEV)

settings = Settings()
