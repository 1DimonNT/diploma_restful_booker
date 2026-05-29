import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    API_BASE_URL = os.getenv("API_BASE_URL", "https://api.demoblaze.com")
    UI_BASE_URL = os.getenv("UI_BASE_URL", "https://demoblaze.com")
    UI_TIMEOUT = int(os.getenv("UI_TIMEOUT", 10))
    BROWSER = os.getenv("BROWSER", "chrome")
    BROWSER_VERSION = os.getenv("BROWSER_VERSION", "128.0")
    WINDOW_WIDTH = int(os.getenv("WINDOW_WIDTH", 1920))
    WINDOW_HEIGHT = int(os.getenv("WINDOW_HEIGHT", 1080))
    SELENOID_URL = os.getenv("SELENOID_URL")
    SELENOID_USER = os.getenv("SELENOID_USER")
    SELENOID_PASSWORD = os.getenv("SELENOID_PASSWORD")
    HOLD_BROWSER_OPEN = os.getenv("HOLD_BROWSER_OPEN", "false").lower() == "true"


settings = Settings()