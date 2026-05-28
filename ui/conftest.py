"""
Фикстуры для UI тестов с использованием Selene.
Поддержка локального запуска и Selenoid.
"""

import allure
import pytest
from selene import browser, support
from allure_commons._allure import StepContext
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from config import settings
from utils.logger import log
from utils.attach import add_screenshot, add_page_source, add_video, add_console_logs


def _get_driver(request):
    """Создание и настройка WebDriver (локально или через Selenoid)"""

    browser_name = settings.BROWSER
    log.info(f"🌐 Initializing {browser_name} browser")

    options = ChromeOptions()
    options.add_argument(f"--window-size={settings.WINDOW_WIDTH},{settings.WINDOW_HEIGHT}")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])

    # Проверяем, запуск через Selenoid
    selenoid_url = settings.SELENOID_URL
    if selenoid_url:
        log.info(f"🚀 Running on Selenoid: {selenoid_url}")

        capabilities = {
            "browserName": browser_name,
            "browserVersion": settings.BROWSER_VERSION,
            "selenoid:options": {
                "enableVNC": True,
                "enableVideo": True,
                "videoName": f"{request.node.name}.mp4"
            }
        }

        for key, value in capabilities.items():
            options.set_capability(key, value)

        driver = webdriver.Remote(command_executor=selenoid_url, options=options)
    else:
        log.info("🖥️ Running locally")
        from selenium.webdriver.chrome.service import Service
        from webdriver_manager.chrome import ChromeDriverManager
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

    return driver


@pytest.fixture(scope="function", autouse=True)
def browser_management(request):
    """
    Фикстура для управления браузером.
    """
    log.info("🖥️ Setting up browser...")

    browser.config.base_url = settings.UI_BASE_URL
    browser.config.timeout = settings.UI_TIMEOUT
    browser.config._wait_decorator = support._logging.wait_with(
        context=StepContext
    )

    browser.config.driver = _get_driver(request)

    if hasattr(request, "node"):
        request.node._selene_driver = browser.config.driver
    request.node.driver = browser.config.driver

    log.info(f"✅ Browser started: {settings.BROWSER}")

    yield

    add_screenshot(browser.config.driver, "📸 Final screenshot")
    add_page_source(browser.config.driver)
    add_console_logs(browser.config.driver)

    if settings.SELENOID_URL:
        add_video(browser.config.driver)

    if not settings.HOLD_BROWSER_OPEN:
        log.info("🔒 Closing browser...")
        browser.quit()
        log.info("✅ Browser closed")
    else:
        log.info("ℹ️ Browser left open")