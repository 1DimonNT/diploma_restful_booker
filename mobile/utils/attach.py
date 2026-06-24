from __future__ import annotations

import time

import allure
import requests
from allure_commons.types import AttachmentType


def add_screenshot(driver, name="screenshot"):
    """Добавляет скриншот в Allure отчет"""
    try:
        png = driver.driver.get_screenshot_as_png() if hasattr(driver, "driver") else driver.get_screenshot_as_png()
        allure.attach(body=png, name=name, attachment_type=AttachmentType.PNG, extension=".png")
        print("✅ Скриншот добавлен в отчет")
    except Exception as e:
        allure.attach(f"Failed to take screenshot: {e}", name="screenshot_error", attachment_type=AttachmentType.TEXT)
        print(f"❌ Ошибка при добавлении скриншота: {e}")


def add_console_logs(driver, name="browser_logs"):
    """Добавляет логи браузера в Allure отчет"""
    try:
        web_driver = driver.driver if hasattr(driver, "driver") else driver

        logs = web_driver.get_log("browser")
        if logs:
            log_text = "\n".join([f"[{log['level']}] {log['message']}" for log in logs])
            allure.attach(log_text, name, AttachmentType.TEXT, ".log")
            print(f"✅ {len(logs)} записей лога браузера добавлено")
        else:
            allure.attach("No console logs available", name, AttachmentType.TEXT, ".log")
    except Exception as e:
        allure.attach(f"Could not retrieve console logs: {e}", name, AttachmentType.TEXT, ".log")
        print(f"❌ Ошибка при получении логов: {e}")


def add_page_source(driver, name="page_source"):
    """Добавляет HTML/XML страницы в Allure отчет"""
    try:
        source = driver.driver.page_source if hasattr(driver, "driver") else driver.page_source

        allure.attach(source, name, AttachmentType.HTML, ".html")
        print("✅ Page source добавлен в отчет")
    except Exception as e:
        allure.attach(f"Failed to get page source: {e}", name, AttachmentType.TEXT)
        print(f"❌ Ошибка при добавлении page source: {e}")


def add_video(driver, test_name=None):
    """Add Selenoid video recording to Allure report (как BINARY MP4)"""
    time.sleep(3)

    video_name = test_name if test_name else driver.session_id
    video_url = f"https://ru.selenoid.autotests.cloud/video/{video_name}.mp4"
    video_url_by_session = f"https://ru.selenoid.autotests.cloud/video/{driver.session_id}.mp4"
    video_found = False

    try:
        print(f"🎥 Попытка скачать видео по URL: {video_url}")
        response = requests.get(video_url, timeout=30)
        if response.status_code == 200 and len(response.content) > 10000:
            allure.attach(
                body=response.content,
                name=f"video_{video_name}.mp4",
                attachment_type=AttachmentType.MP4,
                extension=".mp4",
            )
            print(f"✅ Видео добавлено в отчет (по имени теста): {video_name}")
            video_found = True
    except Exception as e:
        print(f"❌ Ошибка при скачивании видео по имени теста: {e}")

    if not video_found:
        try:
            print(f"🎥 Попытка скачать видео по session_id: {video_url_by_session}")
            response = requests.get(video_url_by_session, timeout=30)
            if response.status_code == 200 and len(response.content) > 10000:
                allure.attach(
                    body=response.content,
                    name=f"video_{driver.session_id}.mp4",
                    attachment_type=AttachmentType.MP4,
                    extension=".mp4",
                )
                print(f"✅ Видео добавлено в отчет (по session_id): {driver.session_id}")
                video_found = True
        except Exception as e:
            print(f"❌ Ошибка при скачивании видео по session_id: {e}")

    if not video_found:
        allure.attach(
            f"ℹ️ Видео не найдено для теста\n"
            f"Test name: {video_name}\n"
            f"Session ID: {driver.session_id}\n"
            f"Проверенные URL:\n"
            f"  - {video_url}\n"
            f"  - {video_url_by_session}\n\n"
            f"Возможные причины:\n"
            f"  - Тест завершился слишком быстро\n"
            f"  - Проблема на стороне Selenoid\n"
            f"  - Видео еще не сгенерировано",
            name="video_not_available",
            attachment_type=AttachmentType.TEXT,
        )
        print("❌ Видео не найдено")


def add_browserstack_video(session_id, login, access_key):
    """Add BrowserStack video recording to Allure report"""
    try:
        browserstack_session = requests.get(
            url=f"https://api.browserstack.com/app-automate/sessions/{session_id}.json",
            auth=(login, access_key),
            timeout=30,
        ).json()

        video_url = browserstack_session["automation_session"]["video_url"]

        response = requests.get(video_url, timeout=60)
        if response.status_code == 200:
            allure.attach(
                body=response.content,
                name=f"browserstack_video_{session_id}.mp4",
                attachment_type=AttachmentType.MP4,
                extension=".mp4",
            )
            print("✅ BrowserStack видео добавлено в отчет")
        else:
            allure.attach(
                f"Video not available: HTTP {response.status_code}",
                name="BrowserStack Video Error",
                attachment_type=AttachmentType.TEXT,
            )
    except Exception as e:
        allure.attach(f"Failed to get video: {e!s}", name="Video Error", attachment_type=AttachmentType.TEXT)
        print(f"❌ Ошибка при добавлении BrowserStack видео: {e}")
