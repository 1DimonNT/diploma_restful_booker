import os
from pathlib import Path

from dotenv import load_dotenv


class Settings:
    """Настройки проекта (без Pydantic)"""

    def __init__(self):
        self._load_mobile_context()
        self._load_ui_settings()

    def _load_mobile_context(self):
        creds_file = Path(".env.credentials")
        if creds_file.exists():
            load_dotenv(creds_file, override=True)

        context = os.getenv("CONTEXT", "local_emulator")
        context_file = Path(f".env.{context}")

        if context_file.exists():
            load_dotenv(context_file, override=True)
            print(f"✅ Loaded mobile configuration from: {context_file}")

        self.context = os.getenv("CONTEXT", "local_emulator")
        self.browserstack_username = os.getenv("BROWSERSTACK_USERNAME", "")
        self.browserstack_access_key = os.getenv("BROWSERSTACK_ACCESS_KEY", "")
        self.remote_url = os.getenv("REMOTE_URL", "http://hub.browserstack.com/wd/hub")
        self.platform_name = os.getenv("PLATFORM_NAME", "android")
        self.platform_version = os.getenv("PLATFORM_VERSION", "13.0")
        self.device_name = os.getenv("DEVICE_NAME", "Samsung Galaxy S23 Ultra")
        self.udid = os.getenv("UDID", "")
        self.app_path = os.getenv("APP_PATH", "./apps/wikipedia.apk")
        self.app_url = os.getenv("APP_URL", "")
        self.mobile_timeout = float(os.getenv("MOBILE_TIMEOUT", "45.0"))
        self.hold_mobile_browser_open = os.getenv("HOLD_MOBILE_BROWSER_OPEN", "false").lower() == "true"
        self.save_page_source_on_failure = os.getenv("SAVE_PAGE_SOURCE_ON_FAILURE", "true").lower() == "true"

    def _load_ui_settings(self):
        self.API_BASE_URL = os.getenv("API_BASE_URL", "https://api.demoblaze.com")
        self.API_TIMEOUT = int(os.getenv("API_TIMEOUT", "30"))
        self.UI_BASE_URL = os.getenv("UI_BASE_URL", "https://demoblaze.com")
        self.UI_TIMEOUT = int(os.getenv("UI_TIMEOUT", "10"))
        self.BROWSER = os.getenv("BROWSER", "chrome")
        self.BROWSER_VERSION = os.getenv("BROWSER_VERSION", "128.0")
        self.WINDOW_WIDTH = int(os.getenv("WINDOW_WIDTH", "1920"))
        self.WINDOW_HEIGHT = int(os.getenv("WINDOW_HEIGHT", "1080"))
        self.HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
        self.HOLD_BROWSER_OPEN = os.getenv("HOLD_BROWSER_OPEN", "false").lower() == "true"

        # Selenoid настройки
        self.SELENOID_URL = os.getenv("SELENOID_URL")
        self.SELENOID_USER = os.getenv("SELENOID_USER")
        self.SELENOID_PASSWORD = os.getenv("SELENOID_PASSWORD")
        self.SELENOID_VIDEO_URL = os.getenv("SELENOID_VIDEO_URL", "https://ru.selenoid.autotests.cloud/video")

    @property
    def is_bstack(self) -> bool:
        return self.context == "bstack"

    @property
    def is_local_emulator(self) -> bool:
        return self.context == "local_emulator"

    @property
    def is_local_real(self) -> bool:
        return self.context == "local_real"


settings = Settings()
