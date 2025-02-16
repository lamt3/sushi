import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

class Config:
    # Database settings
    POSTGRES_USERNAME = os.getenv("POSTGRES_USERNAME", "postgres")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST", "127.0.0.1")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
    POSTGRES_DB_NAME = os.getenv("POSTGRES_DB_NAME", "postgres")
    SQL_COMMAND_ECHO = os.getenv("SQL_COMMAND_ECHO", "False").lower() == "true" 