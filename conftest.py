"""
Глобальные фикстуры и настройки для всех тестов.
Включает настройку API клиента, логирование и Allure вложения.
"""

import allure
import pytest
from allure_commons.types import AttachmentType

from config import settings
from utils.logger import log


def pytest_configure(config):
    """Настройка pytest перед запуском тестов"""
    log.info("=" * 60)
    log.info("🚀 Starting test execution")
    log.info(f"API Base URL: {settings.API_BASE_URL}")
    log.info(f"UI Base URL: {settings.UI_BASE_URL}")
    log.info("=" * 60)


def pytest_unconfigure(config):
    """Действия после завершения всех тестов"""
    log.info("=" * 60)
    log.info("✅ Test execution completed")
    log.info("=" * 60)


@pytest.fixture(scope="session")
def api_base_url():
    """Фикстура для получения базового URL API"""
    return settings.API_BASE_URL


@pytest.fixture(scope="session")
def ui_base_url():
    """Фикстура для получения базового URL UI"""
    return settings.UI_BASE_URL


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Хук для добавления вложений в Allure отчет при падении теста.
    Автоматически добавляет скриншот, page source и видео (для UI тестов).
    """
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        # Для UI тестов добавляем скриншот
        if hasattr(item, "_selene_driver"):
            driver = item._selene_driver
            try:
                allure.attach(
                    driver.get_screenshot_as_png(), name="screenshot_on_failure", attachment_type=AttachmentType.PNG
                )
                allure.attach(driver.page_source, name="page_source_on_failure", attachment_type=AttachmentType.HTML)
                log.error(f"❌ Test failed: {item.name}")
            except Exception as e:
                log.error(f"Failed to attach screenshot: {e}")


@pytest.fixture(scope="function", autouse=True)
def test_logging(request):
    """Автоматическое логирование начала и конца каждого теста"""
    test_name = request.node.name
    log.info(f"\n{'=' * 50}")
    log.info(f"📝 Starting test: {test_name}")
    log.info(f"{'=' * 50}")

    yield

    log.info(f"\n{'=' * 50}")
    log.info(f"🏁 Finished test: {test_name}")
    log.info(f"{'=' * 50}")
