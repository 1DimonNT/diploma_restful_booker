from __future__ import annotations

import allure
import requests
from allure_commons.types import AttachmentType
from config import settings


def add_screenshot(driver, name='screenshot'):
    """Добавляет скриншот в Allure отчет"""
    try:
        # Для Selene browser
        if hasattr(driver, 'driver'):
            png = driver.driver.get_screenshot_as_png()
        else:
            png = driver.get_screenshot_as_png()
        allure.attach(body=png, name=name, attachment_type=AttachmentType.PNG, extension='.png')
    except Exception as e:
        allure.attach(f"Failed to take screenshot: {e}", name="screenshot_error", attachment_type=AttachmentType.TEXT)


def add_console_logs(driver, name='browser_logs'):
    """Добавляет логи браузера в Allure отчет"""
    try:
        # Для Selene browser
        if hasattr(driver, 'driver'):
            web_driver = driver.driver
        else:
            web_driver = driver

        logs = web_driver.get_log("browser")
        if logs:
            log_text = "\n".join([f"[{log['level']}] {log['message']}" for log in logs])
            allure.attach(log_text, name, AttachmentType.TEXT, '.log')
        else:
            allure.attach("No console logs available", name, AttachmentType.TEXT, '.log')
    except Exception:
        allure.attach("No console logs available", name, AttachmentType.TEXT, '.log')


def add_page_source(driver, name='page_source'):
    """Добавляет HTML/XML страницы в Allure отчет"""
    try:
        if hasattr(driver, 'driver'):
            source = driver.driver.page_source
        else:
            source = driver.page_source
        # Экранируем проблемные символы для XML
        source = source.replace('&', '&amp;')
        allure.attach(source, name, AttachmentType.XML, '.xml')
    except Exception as e:
        allure.attach(f"Failed to get page source: {e}", name, AttachmentType.TEXT)


def add_video(driver):
    """Add Selenoid video recording to Allure report"""
    try:
        session_id = driver.session_id
        video_url = f"{settings.SELENOID_VIDEO_URL}/{session_id}.mp4"

        allure.attach(
            '<html><body>'
            '<video width="100%" height="100%" controls autoplay>'
            f'<source src="{video_url}" type="video/mp4">'
            '</video>'
            '</body></html>',
            name="Video Recording",
            attachment_type=allure.attachment_type.HTML,
        )
    except Exception as e:
        allure.attach(
            f"Failed to get video: {str(e)}",
            name="Video Error",
            attachment_type=allure.attachment_type.TEXT
        )


def add_browserstack_video(session_id, login, access_key):
    """Add BrowserStack video recording to Allure report"""
    try:
        browserstack_session = requests.get(
            url=f"https://api.browserstack.com/app-automate/sessions/{session_id}.json",
            auth=(login, access_key),
            timeout=30
        ).json()

        video_url = browserstack_session["automation_session"]["video_url"]

        allure.attach(
            '<html><body>'
            '<video width="100%" height="100%" controls autoplay>'
            f'<source src="{video_url}" type="video/mp4">'
            '</video>'
            '</body></html>',
            name="BrowserStack Video Recording",
            attachment_type=allure.attachment_type.HTML,
        )
    except Exception as e:
        allure.attach(
            f"Failed to get video: {str(e)}",
            name="Video Error",
            attachment_type=allure.attachment_type.TEXT
        )