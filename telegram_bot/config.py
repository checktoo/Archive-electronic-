import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    WEBHOOK_HOST = os.getenv("WEBHOOK_HOST")
    WEBHOOK_PATH = os.getenv("WEBHOOK_PATH", "/webhook")
    WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}" if WEBHOOK_HOST else None
    WEB_SERVER_HOST = os.getenv("WEB_SERVER_HOST", "0.0.0.0")
    WEB_SERVER_PORT = int(os.getenv("WEB_SERVER_PORT", 8000))

config = Config()