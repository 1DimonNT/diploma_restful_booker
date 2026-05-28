import allure
import requests
import time
from allure_commons.types import AttachmentType
from config import settings


def add_screenshot(driver, name='screenshot'):
    """Добавляет скриншот в Allure отчет"""
    png = driver.get_screenshot_as_png()
    allure.attach(body=png, name=name, attachment_type=AttachmentType.PNG, extension='.png')


def add_console_logs(driver, name='browser_logs'):
    """Добавляет логи браузера в Allure отчет"""
    try:
        log = "".join(f'{text}\n' for text in driver.execute("getLog", {'type': 'browser'})['value'])
        allure.attach(log, name, AttachmentType.TEXT, '.log')
    except Exception:
        allure.attach("No console logs available", name, AttachmentType.TEXT, '.log')


def add_page_source(driver, name='page_source'):
    """Добавляет HTML страницы в Allure отчет"""
    html = driver.page_source
    allure.attach(html, name, AttachmentType.HTML, '.html')


def add_video(driver, name=None):
    """Добавляет видео из Selenoid в отчет Allure"""
    time.sleep(3)

    video_name = name if name else driver.session_id

    # Используем настройки из config
    selenoid_video_url = getattr(settings, 'SELENOID_VIDEO_URL', 'https://ru.selenoid.autotests.cloud/video')
    video_url = f"{selenoid_video_url}/{video_name}.mp4"

    try:
        response = requests.get(video_url, timeout=30)
        if response.status_code == 200 and len(response.content) > 10000:
            allure.attach(
                body=response.content,
                name=f"video_{video_name}",
                attachment_type=AttachmentType.MP4,
                extension='.mp4'
            )
        else:
            allure.attach(
                f"Video not available: {video_url} (status {response.status_code})",
                name="video_not_available",
                attachment_type=AttachmentType.TEXT
            )
    except Exception as e:
        allure.attach(
            f"Failed to download video: {e}\nURL: {video_url}",
            name="video_error",
            attachment_type=AttachmentType.TEXT
        )