import os
from dotenv import load_dotenv
import logging

# Load .env file
load_dotenv()

# ANSI escape codes for colors
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    RESET = '\033[0m'

# Custom formatter with colors
class ColoredFormatter(logging.Formatter):
    FORMATS = {
        logging.ERROR: Colors.RED + '%(levelname)s: %(asctime)s - %(name)s - %(message)s' + Colors.RESET,
        logging.INFO: Colors.GREEN + '%(levelname)s: %(asctime)s - %(name)s - %(message)s' + Colors.RESET,
        # Add other levels if needed
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt='%Y-%m-%d %H:%M:%S')
        return formatter.format(record)

# Configure logging
def setup_logging():
    handler = logging.StreamHandler()
    handler.setFormatter(ColoredFormatter())
    logging.basicConfig(
        level=logging.INFO,
        handlers=[handler]
    )

class Config:
    # Database settings
    POSTGRES_USERNAME = os.getenv("POSTGRES_USERNAME", "postgres")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST", "127.0.0.1")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
    POSTGRES_DB_NAME = os.getenv("POSTGRES_DB_NAME", "postgres")
    SQL_COMMAND_ECHO = os.getenv("SQL_COMMAND_ECHO", "False").lower() == "true" 

    # fb configs
    FB_REDIRECT_URI = os.getenv("FB_REDIRECT_URI")
    FB_CLIENT_ID = os.getenv("FB_CLIENT_ID")
    FB_CLIENT_SECRET = os.getenv("FB_CLIENT_SECRET")

    TIKTOK_REDIRECT_URI= os.getenv("TIKTOK_REDIRECT_URI")
    TIKTOK_CLIENT_ID = os.getenv("TIKTOK_CLIENT_ID")
    TIKTOK_CLIENT_SECRET = os.getenv("TIKTOK_CLIENT_SECRET")

    #jwt configs
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key")
    JWT_ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 262800

    #open ai configs
    OPEN_AI_KEY = os.getenv("OPEN_AI_KEY", "")

    # GOOGLE_APPLICATION_CREDENTIALS = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
