from __future__ import annotations

import allure
import re
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
        print("✅ Скриншот добавлен в отчет")
    except Exception as e:
        allure.attach(f"Failed to take screenshot: {e}", name="screenshot_error", attachment_type=AttachmentType.TEXT)
        print(f"❌ Ошибка при добавлении скриншота: {e}")


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
            print(f"✅ {len(logs)} записей лога браузера добавлено")
        else:
            allure.attach("No console logs available", name, AttachmentType.TEXT, '.log')
    except Exception as e:
        allure.attach(f"Could not retrieve console logs: {e}", name, AttachmentType.TEXT, '.log')
        print(f"❌ Ошибка при получении логов: {e}")


def add_page_source(driver, name='page_source'):
    """Добавляет HTML/XML страницы в Allure отчет"""
    try:
        if hasattr(driver, 'driver'):
            source = driver.driver.page_source
        else:
            source = driver.page_source

        # Экранируем проблемные символы для XML
        source = source.replace('&', '&amp;')

        # Исправляем незакрытые теги link
        source = re.sub(r'<link\s+([^>]*?)(?<!/)>', r'<link \1/>', source)

        # Исправляем незакрытые теги meta
        source = re.sub(r'<meta\s+([^>]*?)(?<!/)>', r'<meta \1/>', source)

        # Исправляем незакрытые теги img (для полноты)
        source = re.sub(r'<img\s+([^>]*?)(?<!/)>', r'<img \1/>', source)

        # Исправляем незакрытые теги input
        source = re.sub(r'<input\s+([^>]*?)(?<!/)>', r'<input \1/>', source)

        # Исправляем незакрытые теги br
        source = re.sub(r'<br\s*>', r'<br/>', source)
        source = re.sub(r'<br\s+>', r'<br/>', source)

        # Исправляем незакрытые теги hr
        source = re.sub(r'<hr\s*>', r'<hr/>', source)
        source = re.sub(r'<hr\s+>', r'<hr/>', source)

        allure.attach(source, name, AttachmentType.XML, '.xml')
        print("✅ Page source добавлен в отчет")
    except Exception as e:
        allure.attach(f"Failed to get page source: {e}", name, AttachmentType.TEXT)
        print(f"❌ Ошибка при добавлении page source: {e}")


def add_video(driver):
    """Add Selenoid video recording to Allure report"""
    try:
        # Получаем session_id из драйвера
        session_id = driver.session_id
        # Формируем прямую ссылку на видео Selenoid
        video_url = f"https://ru.selenoid.autotests.cloud/video/{session_id}.mp4"

        print(f"🎥 Видео URL: {video_url}")

        allure.attach(
            f'<html><body><video width="100%" height="100%" controls autoplay>'
            f'<source src="{video_url}" type="video/mp4">'
            f'Your browser does not support the video tag.</video></body></html>',
            name="Video Recording",
            attachment_type=allure.attachment_type.HTML,
        )
        print("✅ Видео добавлено в отчет")
    except Exception as e:
        allure.attach(str(e), name="Video Error", attachment_type=allure.attachment_type.TEXT)
        print(f"❌ Ошибка при добавлении видео: {e}")


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
            'Your browser does not support the video tag.'
            '</video>'
            '</body></html>',
            name="BrowserStack Video Recording",
            attachment_type=allure.attachment_type.HTML,
        )
        print("✅ BrowserStack видео добавлено в отчет")
    except Exception as e:
        allure.attach(
            f"Failed to get video: {str(e)}",
            name="Video Error",
            attachment_type=allure.attachment_type.TEXT
        )
        print(f"❌ Ошибка при добавлении BrowserStack видео: {e}")