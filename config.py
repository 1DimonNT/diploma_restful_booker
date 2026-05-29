import os
from pathlib import Path
from typing import Optional
from pydantic import BaseSettings
from dotenv import load_dotenv


class Settings(BaseSettings):
    """Настройки проекта через Pydantic"""

    # ========== API Settings ==========
    API_BASE_URL: str = "https://api.demoblaze.com"
    API_TIMEOUT: int = 30

    # ========== UI Settings ==========
    UI_BASE_URL: str = "https://demoblaze.com"
    UI_TIMEOUT: int = 10
    BROWSER: str = "chrome"
    BROWSER_VERSION: str = "128.0"
    WINDOW_WIDTH: int = 1920
    WINDOW_HEIGHT: int = 1080
    HEADLESS: bool = False
    HOLD_BROWSER_OPEN: bool = False

    # ========== Selenoid ==========
    SELENOID_URL: Optional[str] = None
    SELENOID_USER: Optional[str] = None
    SELENOID_PASSWORD: Optional[str] = None
    SELENOID_VIDEO_URL: str = "https://ru.selenoid.autotests.cloud/video"

    # ========== Mobile Settings ==========
    context: str = "local_emulator"
    browserstack_username: str = ""
    browserstack_access_key: str = ""
    remote_url: str = "http://hub.browserstack.com/wd/hub"
    platform_name: str = "android"
    platform_version: str = "13.0"
    device_name: str = "Samsung Galaxy S23 Ultra"
    udid: str = ""
    app_path: str = "./apps/wikipedia.apk"
    app_url: str = ""
    mobile_timeout: float = 45.0
    hold_mobile_browser_open: bool = False
    save_page_source_on_failure: bool = True

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._load_mobile_context()

    def _load_mobile_context(self):
        creds_file = Path(".env.credentials")
        if creds_file.exists():
            load_dotenv(creds_file, override=True)

        context = os.getenv("CONTEXT", self.context)
        context_file = Path(f".env.{context}")

        if context_file.exists():
            load_dotenv(context_file, override=True)
            print(f"✅ Loaded mobile configuration from: {context_file}")

        self.context = os.getenv("CONTEXT", self.context)
        self.browserstack_username = os.getenv("BROWSERSTACK_USERNAME", self.browserstack_username)
        self.browserstack_access_key = os.getenv("BROWSERSTACK_ACCESS_KEY", self.browserstack_access_key)
        self.remote_url = os.getenv("REMOTE_URL", self.remote_url)
        self.platform_name = os.getenv("PLATFORM_NAME", self.platform_name)
        self.platform_version = os.getenv("PLATFORM_VERSION", self.platform_version)
        self.device_name = os.getenv("DEVICE_NAME", self.device_name)
        self.udid = os.getenv("UDID", self.udid)
        self.app_path = os.getenv("APP_PATH", self.app_path)
        self.app_url = os.getenv("APP_URL", self.app_url)
        self.mobile_timeout = float(os.getenv("MOBILE_TIMEOUT", self.mobile_timeout))

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