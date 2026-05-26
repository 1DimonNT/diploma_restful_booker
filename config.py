"""
Конфигурация проекта с использованием Pydantic Settings.
Управление переменными окружения и настройками для разных окружений.
"""

from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional


class ApiSettings(BaseSettings):
    """Настройки API"""

    base_url: str = Field(default="https://api.demoblaze.com", alias="API_BASE_URL")
    timeout: int = Field(default=30, alias="API_TIMEOUT")

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
        "extra": "ignore"
    }

    @property
    def full_base_url(self) -> str:
        return self.base_url


class UISettings(BaseSettings):
    """Настройки UI тестов"""

    base_url: str = Field(default="https://demoblaze.com", alias="UI_BASE_URL")
    timeout: float = Field(default=10.0, alias="UI_TIMEOUT")
    browser: str = Field(default="chrome", alias="BROWSER")
    browser_version: str = Field(default="128.0", alias="BROWSER_VERSION")
    window_width: int = Field(default=1920, alias="WINDOW_WIDTH")
    window_height: int = Field(default=1080, alias="WINDOW_HEIGHT")
    headless: bool = Field(default=False, alias="HEADLESS")
    hold_browser_open: bool = Field(default=False, alias="HOLD_BROWSER_OPEN")
    save_page_source_on_failure: bool = Field(default=True, alias="SAVE_PAGE_SOURCE_ON_FAILURE")

    # Selenoid настройки
    selenoid_url: Optional[str] = Field(default=None, alias="SELENOID_URL")
    selenoid_user: Optional[str] = Field(default=None, alias="SELENOID_USER")
    selenoid_password: Optional[str] = Field(default=None, alias="SELENOID_PASSWORD")

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
        "extra": "ignore"
    }


class MobileSettings(BaseSettings):
    """Настройки Mobile тестов"""

    use_browserstack: bool = Field(default=False, alias="USE_BROWSERSTACK")
    browserstack_username: Optional[str] = Field(default=None, alias="BROWSERSTACK_USERNAME")
    browserstack_access_key: Optional[str] = Field(default=None, alias="BROWSERSTACK_ACCESS_KEY")
    browserstack_app_url: Optional[str] = Field(default=None, alias="BROWSERSTACK_APP_URL")

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
        "extra": "ignore"
    }


class Settings(BaseSettings):
    """Главный класс настроек"""

    api: ApiSettings = Field(default_factory=ApiSettings)
    ui: UISettings = Field(default_factory=UISettings)
    mobile: MobileSettings = Field(default_factory=MobileSettings)

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
        "extra": "ignore"
    }


# Создаем глобальный объект настроек
settings = Settings()