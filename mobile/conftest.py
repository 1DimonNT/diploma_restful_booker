from __future__ import annotations

import allure
import allure_commons
import pytest
from appium import webdriver
from selene import browser, support
from selenium.webdriver.remote.remote_connection import RemoteConnection

import mobile.config as config
from utils import attach


def pytest_addoption(parser):
    """Add command line options for pytest"""
    parser.addoption(
        "--platform",
        action="store",
        default="android",
        choices=["android", "ios"],
        help="Platform to run tests on: android or ios"
    )
    parser.addoption(
        "--context",
        action="store",
        default=None,
        help="Override context: local_emulator, local_real, bstack"
    )


def pytest_configure(config):
    """Register custom markers"""
    config.addinivalue_line("markers", "android: mark test to run only on Android platform")
    config.addinivalue_line("markers", "ios: mark test to run only on iOS platform")
    config.addinivalue_line("markers", "local: mark test to run only on local devices")
    config.addinivalue_line("markers", "bstack: mark test to run only on BrowserStack")
    config.addinivalue_line("markers", "onboarding: tests for onboarding screens")
    config.addinivalue_line("markers", "search: tests for search functionality")
    config.addinivalue_line("markers", "article: tests for article viewing")


@pytest.fixture(scope="session")
def platform(request):
    """Return platform from command line"""
    return request.config.getoption("--platform")


@pytest.fixture(scope="function", autouse=True)
def mobile_management(request, platform):
    """Main fixture for mobile driver management"""

    # Override context if provided via command line
    context = request.config.getoption("--context")
    if context:
        import os
        os.environ["CONTEXT"] = context
        # Reload settings with new context
        config.settings._load_context_config()

    # Get driver options based on platform
    driver_options = config.get_driver_options(platform)

    # Determine remote URL
    if config.settings.is_bstack:
        remote_url = config.settings.remote_url
        print(f"\n🚀 Running on BrowserStack: {config.settings.device_name}")
    else:
        # Local execution (emulator or real device)
        remote_url = "http://localhost:4723/wd/hub"
        print(f"\n🚀 Running locally: {config.settings.device_name} ({config.settings.context})")

    # Configure Selene
    browser.config.driver = webdriver.Remote(remote_url, options=driver_options)
    browser.config.timeout = config.settings.timeout

    # Enable Allure steps in Selene logs
    browser.config._wait_decorator = support._logging.wait_with(
        context=allure_commons._allure.StepContext
    )

    # Print session info
    session_id = browser.driver.session_id
    print(f"📱 Session ID: {session_id}")

    if config.settings.is_bstack:
        session_url = f"https://app-automate.browserstack.com/dashboard/v2/builds/sessions/{session_id}"
        print(f"🔗 BrowserStack session: {session_url}")
        allure.attach(
            f"<a href='{session_url}'>BrowserStack Session Link</a>",
            name="BrowserStack Session",
            attachment_type=allure.attachment_type.HTML
        )

    yield

    # Teardown
    if not config.settings.hold_browser_open:
        print("\n📱 Closing driver session...")

        # Attach artifacts only on failure
        if hasattr(request, "node") and request.node.rep_call and request.node.rep_call.failed:
            attach.add_screenshot(browser)
            attach.add_xml(browser)

            if config.settings.is_bstack:
                attach.add_video(
                    session_id,
                    config.settings.browserstack_username,
                    config.settings.browserstack_access_key
                )

        browser.quit()
        print("✅ Driver session closed")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test result for teardown decisions"""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
    return rep