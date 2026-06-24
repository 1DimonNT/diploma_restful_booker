from __future__ import annotations

import os

import allure
import allure_commons
import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from selene import browser, support

from config import settings
from utils import attach


def pytest_addoption(parser):
    parser.addoption(
        "--platform",
        action="store",
        default="android",
        choices=["android", "ios"],
        help="Platform to run tests on: android or ios",
    )
    parser.addoption(
        "--context", action="store", default=None, help="Override context: local_emulator, local_real, bstack"
    )


def pytest_configure(config):
    config.addinivalue_line("markers", "android: mark test to run only on Android platform")
    config.addinivalue_line("markers", "ios: mark test to run only on iOS platform")
    config.addinivalue_line("markers", "local: mark test to run only on local devices")
    config.addinivalue_line("markers", "bstack: mark test to run only on BrowserStack")
    config.addinivalue_line("markers", "onboarding: tests for onboarding screens")
    config.addinivalue_line("markers", "search: tests for search functionality")
    config.addinivalue_line("markers", "article: tests for article viewing")


@pytest.fixture(scope="session")
def platform(request):
    return request.config.getoption("--platform")


def get_driver_options():
    """Получение опций драйвера с поддержкой BrowserStack и локального запуска"""
    options = UiAutomator2Options()

    capabilities = {
        "platformName": settings.platform_name,
        "platformVersion": settings.platform_version,
        "deviceName": settings.device_name,
        "appWaitActivity": "org.wikipedia.*",
        "automationName": "UiAutomator2",
        "noReset": False,
        "fullReset": False,
    }

    if settings.is_bstack:
        # Берем ключи из settings (которые загружаются из переменных окружения)
        username = settings.browserstack_username or os.environ.get("BROWSERSTACK_USERNAME")
        access_key = settings.browserstack_access_key or os.environ.get("BROWSERSTACK_ACCESS_KEY")
        app_url = settings.app_url or os.environ.get("APP_URL")

        if username and access_key and app_url:
            capabilities["app"] = app_url
            capabilities["bstack:options"] = {
                "userName": username,
                "accessKey": access_key,
                "projectName": "Mobile QA Automation Project",
                "buildName": f"Wikipedia {settings.context.capitalize()} Tests",
                "sessionName": f"Test on {settings.device_name} ({settings.context})",
                "local": "false",
                "debug": "true",
                "networkLogs": "true",
                "consoleLogs": "info",
            }
            print(f"✅ BrowserStack auth with user: {username}")
        else:
            print("\n❌ BrowserStack credentials not found!")
            print(f"  USERNAME: {username}")
            print(f"  ACCESS_KEY: {'***' if access_key else 'None'}")
            print(f"  APP_URL: {app_url}")

    options.load_capabilities(capabilities)
    return options


@pytest.fixture(scope="function", autouse=True)
def mobile_management(request, platform):
    context = request.config.getoption("--context")
    if context:
        os.environ["CONTEXT"] = context

    driver_options = get_driver_options()

    if settings.is_bstack:
        remote_url = settings.remote_url
        print(f"\nRunning on BrowserStack: {settings.device_name}")
    else:
        remote_url = "http://localhost:4723/wd/hub"
        print(f"\nRunning locally: {settings.device_name} ({settings.context})")

    browser.config.driver = webdriver.Remote(remote_url, options=driver_options)
    browser.config.timeout = settings.mobile_timeout

    browser.config._wait_decorator = support._logging.wait_with(context=allure_commons._allure.StepContext)

    session_id = browser.driver.session_id
    print(f"Session ID: {session_id}")

    if settings.is_bstack:
        session_url = f"https://app-automate.browserstack.com/dashboard/v2/builds/sessions/{session_id}"
        print(f"BrowserStack session: {session_url}")
        allure.attach(
            f"<a href='{session_url}'>BrowserStack Session Link</a>",
            name="BrowserStack Session",
            attachment_type=allure.attachment_type.HTML,
        )

    yield

    if not settings.hold_mobile_browser_open:
        print("\nClosing driver session...")

        if hasattr(request, "node") and request.node.rep_call and request.node.rep_call.failed:
            attach.add_screenshot(browser)
            attach.add_page_source(browser)

            if settings.is_bstack:
                attach.add_video(browser)
        browser.quit()
        print("Driver session closed")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
    return rep