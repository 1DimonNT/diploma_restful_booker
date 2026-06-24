from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Настройки проекта с валидацией через Pydantic"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # API
    api_base_url: str = Field(default="https://api.demoblaze.com", alias="API_BASE_URL")
    api_timeout: int = Field(default=30, alias="API_TIMEOUT")

    # UI
    ui_base_url: str = Field(default="https://demoblaze.com", alias="UI_BASE_URL")
    ui_timeout: int = Field(default=10, alias="UI_TIMEOUT")
    browser: str = Field(default="chrome", alias="BROWSER")
    browser_version: str = Field(default="128.0", alias="BROWSER_VERSION")
    window_width: int = Field(default=1920, alias="WINDOW_WIDTH")
    window_height: int = Field(default=1080, alias="WINDOW_HEIGHT")
    headless: bool = Field(default=False, alias="HEADLESS")
    selenoid_url: str | None = Field(default=None, alias="SELENOID_URL")
    selenoid_user: str | None = Field(default=None, alias="SELENOID_USER")
    selenoid_password: str | None = Field(default=None, alias="SELENOID_PASSWORD")
    hold_browser_open: bool = Field(default=False, alias="HOLD_BROWSER_OPEN")

    # Mobile (BrowserStack)
    context: str = Field(default="local_emulator", alias="CONTEXT")
    browserstack_username: str | None = Field(default=None, alias="BROWSERSTACK_USERNAME")
    browserstack_access_key: str | None = Field(default=None, alias="BROWSERSTACK_ACCESS_KEY")
    remote_url: str = Field(default="http://hub.browserstack.com/wd/hub", alias="REMOTE_URL")
    platform_name: str = Field(default="android", alias="PLATFORM_NAME")
    platform_version: str = Field(default="13.0", alias="PLATFORM_VERSION")
    device_name: str = Field(default="Samsung Galaxy S23 Ultra", alias="DEVICE_NAME")
    app_url: str | None = Field(default=None, alias="APP_URL")
    mobile_timeout: float = Field(default=45.0, alias="MOBILE_TIMEOUT")
    hold_mobile_browser_open: bool = Field(default=False, alias="HOLD_MOBILE_BROWSER_OPEN")

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
