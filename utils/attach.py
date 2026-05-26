"""
Вспомогательные функции для добавления вложений в Allure отчет.
"""

import allure
import logging
from allure_commons.types import AttachmentType
import re


def add_screenshot(driver, name="📸 Screenshot"):
    try:
        screenshot = driver.get_screenshot_as_png()
        allure.attach(body=screenshot, name=name, attachment_type=AttachmentType.PNG)
    except Exception as e:
        logging.error(f"Failed to take screenshot: {e}")


def add_page_source(driver, name="📄 Page Source"):
    try:
        page_source = driver.page_source
        allure.attach(body=page_source, name=name, attachment_type=AttachmentType.HTML)
    except Exception as e:
        logging.error(f"Failed to capture page source: {e}")


def add_console_logs(driver, name="📜 Console Logs"):
    try:
        logs = driver.get_log("browser")
        if logs:
            log_text = "\n".join([f"[{log['level']}] {log['message']}" for log in logs])
            log_text = re.sub(r'[^\x20-\x7E\n\r\t]', '', log_text)
            allure.attach(body=log_text, name=name, attachment_type=AttachmentType.TEXT)
    except Exception as e:
        logging.error(f"Failed to capture console logs: {e}")


def add_video(driver, name="🎥 Video"):
    try:
        session_id = driver.session_id
        executor_url = driver.command_executor._url
        selenoid_host = executor_url.replace('/wd/hub', '').split('@')[-1]
        video_url = f"https://{selenoid_host}/video/{session_id}.mp4"

        html = f"""
        <html>
            <body>
                <video width="100%" height="100%" controls>
                    <source src="{video_url}" type="video/mp4">
                </video>
            </body>
        </html>
        """
        allure.attach(body=html, name=name, attachment_type=AttachmentType.HTML)
    except Exception as e:
        logging.error(f"Failed to attach video: {e}")