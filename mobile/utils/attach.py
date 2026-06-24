from __future__ import annotations

import allure
import requests
from allure_commons.types import AttachmentType


def add_screenshot(driver, name="screenshot"):
    """Добавляет скриншот в Allure отчет"""
    try:
        png = driver.driver.get_screenshot_as_png() if hasattr(driver, "driver") else driver.get_screenshot_as_png()
        allure.attach(body=png, name=name, attachment_type=AttachmentType.PNG, extension=".png")
        print("Screenshot added to report")
    except Exception as e:
        allure.attach(f"Failed to take screenshot: {e}", name="screenshot_error", attachment_type=AttachmentType.TEXT)
        print(f"Error adding screenshot: {e}")


def add_page_source(driver, name="page_source"):
    """Добавляет XML страницы в Allure отчет"""
    try:
        source = driver.driver.page_source if hasattr(driver, "driver") else driver.page_source
        allure.attach(source, name, AttachmentType.XML, ".xml")
        print("Page source added to report")
    except Exception as e:
        allure.attach(f"Failed to get page source: {e}", name, AttachmentType.TEXT)
        print(f"Error adding page source: {e}")


def add_video(driver):
    """Добавляет видео из BrowserStack в Allure отчет"""
    try:
        session_id = driver.driver.session_id
        login = driver.driver.capabilities.get("bstack:options", {}).get("userName")
        access_key = driver.driver.capabilities.get("bstack:options", {}).get("accessKey")

        if not login or not access_key:
            print("BrowserStack credentials not found, skipping video")
            return

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
            print("BrowserStack video added to report")
        else:
            allure.attach(
                f"Video not available: HTTP {response.status_code}",
                name="BrowserStack Video Error",
                attachment_type=AttachmentType.TEXT,
            )
    except Exception as e:
        allure.attach(
            f"Failed to get video: {e!s}",
            name="Video Error",
            attachment_type=AttachmentType.TEXT,
        )
        print(f"Error adding BrowserStack video: {e}")
