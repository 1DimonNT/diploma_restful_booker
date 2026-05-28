from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions


class Settings(BaseSettings):
    # Context (local_emulator, local_real, bstack)
    context: str = "local_emulator"

    # BrowserStack credentials (for bstack context)
    browserstack_username: str = ""
    browserstack_access_key: str = ""
    remote_url: str = "http://hub.browserstack.com/wd/hub"

    # Platform capabilities
    platform_name: str = "android"
    platform_version: str = "13.0"
    device_name: str = "Samsung Galaxy S23 Ultra"

    # For local real device
    udid: str = ""

    # App configuration
    app_path: str = "./apps/wikipedia.apk"
    app_url: str = ""

    # Timeouts
    timeout: float = 45.0

    # Browser management
    hold_browser_open: bool = False
    save_page_source_on_failure: bool = True

    # Allure
    allure_results_dir: str = "allure-results"

    class Config:
        env_file_encoding = "utf-8"
        extra = "ignore"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._load_context_config()

    def _load_context_config(self):
        """Load configuration based on CONTEXT environment variable"""
        # First, load credentials if they exist
        creds_file = Path(".env.credentials")
        if creds_file.exists():
            load_dotenv(creds_file, override=True)

        # Then load context-specific config
        context = os.getenv("CONTEXT", self.context)
        context_file = Path(f".env.{context}")

        if context_file.exists():
            load_dotenv(context_file, override=True)
            print(f"✅ Loaded configuration from: {context_file}")
        else:
            print(f"⚠️ Warning: Context file {context_file} not found, using defaults")

        # Reload values from environment
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
        self.timeout = float(os.getenv("TIMEOUT", self.timeout))
        self.hold_browser_open = os.getenv("HOLD_BROWSER_OPEN", "false").lower() == "true"
        self.save_page_source_on_failure = os.getenv("SAVE_PAGE_SOURCE_ON_FAILURE", "true").lower() == "true"
        self.allure_results_dir = os.getenv("ALLURE_RESULTS_DIR", self.allure_results_dir)

    @property
    def is_bstack(self) -> bool:
        """Check if running on BrowserStack"""
        return self.context == "bstack"

    @property
    def is_local_emulator(self) -> bool:
        """Check if running on local emulator"""
        return self.context == "local_emulator"

    @property
    def is_local_real(self) -> bool:
        """Check if running on real device"""
        return self.context == "local_real"

    @property
    def driver_options_android(self) -> UiAutomator2Options:
        """Configure Android driver options"""
        options = UiAutomator2Options()

        capabilities = {
            "platformName": self.platform_name,
            "platformVersion": self.platform_version,
            "deviceName": self.device_name,
            "appWaitActivity": "org.wikipedia.*",
            "automationName": "UiAutomator2",
            "noReset": False,
            "fullReset": False,
        }

        # Add UDID for real device
        if self.is_local_real and self.udid:
            capabilities["udid"] = self.udid

        # Add app path for local execution
        if self.is_local_emulator or self.is_local_real:
            if Path(self.app_path).exists():
                capabilities["app"] = str(Path(self.app_path).absolute())
            else:
                print(f"⚠️ Warning: App not found at {self.app_path}")

        # Add app URL for BrowserStack
        if self.is_bstack and self.app_url:
            capabilities["app"] = self.app_url

            # Add BrowserStack options
            capabilities["bstack:options"] = {
                "userName": self.browserstack_username,
                "accessKey": self.browserstack_access_key,
                "projectName": "Mobile QA Automation Project",
                "buildName": f"Wikipedia {self.context.capitalize()} Tests",
                "sessionName": f"Test on {self.device_name} ({self.context})",
                "local": "false",
                "debug": "true",
                "networkLogs": "true",
                "consoleLogs": "info",
            }

        options.load_capabilities(capabilities)
        return options

    @property
    def driver_options_ios(self) -> XCUITestOptions:
        """Configure iOS driver options for BrowserStack"""
        options = XCUITestOptions()

        capabilities = {
            "platformName": "ios",
            "platformVersion": "16.0",
            "deviceName": "iPhone 14",
            "automationName": "XCUITest",
        }

        if self.is_bstack:
            capabilities["app"] = self.app_url
            capabilities["bstack:options"] = {
                "userName": self.browserstack_username,
                "accessKey": self.browserstack_access_key,
                "projectName": "Mobile QA Automation Project",
                "buildName": "Wikipedia iOS Tests",
                "sessionName": f"iOS test on iPhone 14 ({self.context})",
                "local": "false",
                "debug": "true",
                "networkLogs": "true",
                "consoleLogs": "info",
            }

        options.load_capabilities(capabilities)
        return options


# Create global settings instance
settings = Settings()


def get_driver_options(platform: str = "android"):
    """Factory function to get driver options for specified platform"""
    if platform.lower() == "android":
        return settings.driver_options_android
    elif platform.lower() == "ios":
        return settings.driver_options_ios
    else:
        raise ValueError(f"Unsupported platform: {platform}")