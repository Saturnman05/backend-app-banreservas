from dotenv import load_dotenv
import os

load_dotenv()

DEV = "development"
ENV = os.getenv("ENVIRONMENT", DEV)
