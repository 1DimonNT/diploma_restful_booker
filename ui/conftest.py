"""
Фикстуры для UI тестов с использованием Selene.
Поддержка локального запуска и Selenoid.
"""

import allure
import pytest
from allure_commons._allure import StepContext
from selene import browser, support
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions

from config import settings
from utils.attach import add_console_logs, add_page_source, add_screenshot, add_video
from utils.logger import log


def _get_driver(request):
    """Создание и настройка WebDriver (локально или через Selenoid)"""

    browser_name = settings.browser
    log.info(f"Initializing {browser_name} browser")

    options = ChromeOptions()
    options.add_argument(f"--window-size={settings.window_width},{settings.window_height}")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    selenoid_url = settings.selenoid_url
    if selenoid_url and selenoid_url.strip():
        log.info(f"Running on Selenoid: {selenoid_url}")

        capabilities = {
            "browserName": browser_name,
            "browserVersion": settings.browser_version,
            "selenoid:options": {
                "enableVNC": True,
                "enableVideo": True,
                "videoName": f"{request.node.name}_{request.node.nodeid}.mp4",
                "videoScreenSize": f"{settings.window_width}x{settings.window_height}",
                "videoFrameRate": 24,
                "sessionTimeout": "10m",
            },
        }

        for key, value in capabilities.items():
            options.set_capability(key, value)

        command_executor = selenoid_url.rstrip("/")
        if not command_executor.endswith("/wd/hub"):
            command_executor += "/wd/hub"

        driver = webdriver.Remote(command_executor=command_executor, options=options)
    else:
        log.info("Running locally")
        from selenium.webdriver.chrome.service import Service
        from webdriver_manager.chrome import ChromeDriverManager

        driver_path = ChromeDriverManager().install()
        log.info(f"Driver path: {driver_path}")

        service = Service(driver_path)
        driver = webdriver.Chrome(service=service, options=options)

    return driver


@pytest.fixture(scope="function", autouse=True)
def browser_management(request):
    """
    Фикстура для управления браузером.
    """
    log.info("Setting up browser...")

    browser.config.base_url = settings.ui_base_url
    browser.config.timeout = settings.ui_timeout
    browser.config._wait_decorator = support._logging.wait_with(context=StepContext)

    browser.config.driver = _get_driver(request)

    if hasattr(request, "node"):
        request.node._selene_driver = browser.config.driver
    request.node.driver = browser.config.driver

    log.info(f"Browser started: {settings.browser}")

    yield

    add_screenshot(browser.config.driver, "Final screenshot")
    add_page_source(browser.config.driver)
    add_console_logs(browser.config.driver)

    if settings.selenoid_url:
        add_video(browser.config.driver, test_name=request.node.name)

    if not settings.hold_browser_open:
        log.info("Closing browser...")
        browser.quit()
        log.info("Browser closed")
    else:
        log.info("Browser left open")


@pytest.fixture(scope="function", autouse=True)
def clear_browser_state():
    """
    Очищает состояние браузера между тестами (cookies, localStorage, sessionStorage)
    """
    yield
    try:
        browser.driver.delete_all_cookies()
        browser.driver.execute_script("window.localStorage.clear();")
        browser.driver.execute_script("window.sessionStorage.clear();")
        log.debug("Browser state cleared between tests")
    except Exception as e:
        log.warning(f"Failed to clear browser state: {e}")


@pytest.fixture(scope="function")
def open_main_page():
    """Фикстура для открытия главной страницы"""
    with allure.step("Opening main page"):
        browser.open("/")
        log.info(f"Opened: {settings.ui_base_url}")
        return browser
