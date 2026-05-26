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
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from config import settings
from utils.logger import log
from utils.attach import add_screenshot, add_page_source, add_video, add_console_logs


def _get_driver(request):
    """Создание и настройка WebDriver (локально или через Selenoid)"""

    browser_name = settings.ui.browser.lower()
    log.info(f"🌐 Initializing {browser_name} browser")

    # Базовые опции для Chrome
    if browser_name == "chrome":
        options = ChromeOptions()
        if settings.ui.headless:
            options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_argument(f"--window-size={settings.ui.window_width},{settings.ui.window_height}")
    else:
        raise ValueError(f"Unsupported browser: {browser_name}")

    # Проверяем, запуск через Selenoid или локально
    if settings.ui.selenoid_url:
        log.info(f"🚀 Running on Selenoid: {settings.ui.selenoid_url}")

        capabilities = {
            "browserName": browser_name,
            "browserVersion": settings.ui.browser_version,
            "selenoid:options": {
                "enableVNC": True,
                "enableVideo": True,
                "videoName": f"{request.node.name}.mp4"
            }
        }

        for key, value in capabilities.items():
            options.set_capability(key, value)

        # Формируем URL для Selenoid с авторизацией
        selenoid_host = settings.ui.selenoid_url.replace('https://', '').replace('http://', '').rstrip('/')
        selenoid_url = f'https://{settings.ui.selenoid_user}:{settings.ui.selenoid_password}@{selenoid_host}'

        driver = webdriver.Remote(command_executor=selenoid_url, options=options)
    else:
        log.info("🖥️ Running locally")
        from selenium.webdriver.chrome.service import Service
        from webdriver_manager.chrome import ChromeDriverManager
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

    return driver


@pytest.fixture(scope="session")
def browser_management(request):
    """
    Фикстура для управления браузером на всю сессию тестов.
    Браузер открывается один раз и закрывается после всех тестов.
    """
    log.info("🖥️ Setting up browser for test session...")

    # Настройка Selene
    browser.config.base_url = settings.ui.base_url
    browser.config.timeout = settings.ui.timeout
    browser.config.save_page_source_on_failure = settings.ui.save_page_source_on_failure
    browser.config._wait_decorator = support._logging.wait_with(
        context=StepContext
    )

    # Создание драйвера
    browser.config.driver = _get_driver(request)

    # Сохраняем драйвер в item для доступа в хуке
    if hasattr(request, "node"):
        request.node._selene_driver = browser.config.driver
    request.node.driver = browser.config.driver

    log.info(f"✅ Browser started: {settings.ui.browser}")

    yield

    # Добавляем вложения в Allure
    add_screenshot(browser.config.driver, "📸 Final screenshot")
    add_page_source(browser.config.driver)
    add_console_logs(browser.config.driver)

    if settings.ui.selenoid_url:
        add_video(browser.config.driver)

    # Закрытие браузера после всех тестов
    if not settings.ui.hold_browser_open:
        log.info("🔒 Closing browser...")
        browser.quit()
        log.info("✅ Browser closed")
    else:
        log.info("ℹ️ Browser left open (HOLD_BROWSER_OPEN=true)")


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
        log.info(f"Opened: {settings.ui.base_url}")
        return browser