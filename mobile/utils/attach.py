from __future__ import annotations

import allure
import requests


def add_screenshot(browser):
    """Add screenshot to Allure report"""
    png = browser.driver.get_screenshot_as_png()
    allure.attach(
        body=png,
        name="Screenshot",
        attachment_type=allure.attachment_type.PNG
    )


def add_xml(browser):
    """Add page source XML to Allure report"""
    xml_dump = browser.driver.page_source
    allure.attach(
        body=xml_dump,
        name="Page Source (XML)",
        attachment_type=allure.attachment_type.XML
    )


def add_video(session_id, login, access_key):
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
            name="Video Recording",
            attachment_type=allure.attachment_type.HTML,
        )
    except Exception as e:
        allure.attach(
            f"Failed to get video: {str(e)}",
            name="Video Error",
            attachment_type=allure.attachment_type.TEXT
        )


def add_session_link(session_id, username, access_key):
    """Add BrowserStack session link to Allure report"""
    try:
        browserstack_session = requests.get(
            url=f"https://api.browserstack.com/app-automate/sessions/{session_id}.json",
            auth=(username, access_key),
            timeout=30
        ).json()

        session_url = browserstack_session["automation_session"]["public_url"]

        allure.attach(
            f"<a href='{session_url}'>BrowserStack Session</a>",
            name="BrowserStack Session Link",
            attachment_type=allure.attachment_type.HTML
        )
    except Exception:
        pass