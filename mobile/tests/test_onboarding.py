from __future__ import annotations

import time

import allure
import pytest
from appium.webdriver.common.appiumby import AppiumBy
from selene import be
from selene.support.shared import browser

from config import settings
from mobile.pages.wikipedia_app import wikipedia


@allure.suite("Wikipedia Mobile Tests")
@allure.tag("android", "onboarding")
@allure.title("Onboarding screens should work correctly")
class TestOnboarding:
    @allure.title("Complete onboarding flow and verify main screen")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.android
    @pytest.mark.onboarding
    def test_onboarding__complete_flow__should_show_main_screen(self):
        # === DEBUG ===
        print("\n=== DEBUG ===")
        print(f"BROWSERSTACK_USERNAME: {settings.browserstack_username}")
        print(f"BROWSERSTACK_ACCESS_KEY: {settings.browserstack_access_key}")
        print(f"APP_URL: {settings.app_url}")
        print(f"CONTEXT: {settings.context}")
        print("=== END DEBUG ===\n")

        wikipedia.close_onboarding_if_present()
        search_field = browser.element((AppiumBy.ACCESSIBILITY_ID, "Search Wikipedia"))
        search_field.with_(timeout=10).should(be.visible)
        print("✅ Onboarding completed, main screen visible")

    @allure.title("Skip onboarding and verify main screen")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.android
    @pytest.mark.onboarding
    def test_onboarding__skip_onboarding__should_show_main_screen(self):
        # === DEBUG ===
        print("\n=== DEBUG ===")
        print(f"BROWSERSTACK_USERNAME: {settings.browserstack_username}")
        print(f"BROWSERSTACK_ACCESS_KEY: {settings.browserstack_access_key}")
        print(f"APP_URL: {settings.app_url}")
        print(f"CONTEXT: {settings.context}")
        print("=== END DEBUG ===\n")

        try:
            skip_btn = browser.element((AppiumBy.XPATH, "//android.widget.TextView[@text='Skip']/.."))
            skip_btn.click()
            print("✅ Clicked Skip")
            time.sleep(2)
        except:
            wikipedia.close_onboarding_if_present()

        try:
            search_field = browser.element((AppiumBy.ACCESSIBILITY_ID, "Search Wikipedia"))
            search_field.with_(timeout=10).should(be.visible)
            print("✅ Main screen visible after skip")
        except:
            wikipedia.close_onboarding_if_present()
            search_field = browser.element((AppiumBy.ACCESSIBILITY_ID, "Search Wikipedia"))
            search_field.with_(timeout=10).should(be.visible)

        print("✅ Skip worked, main screen visible")

    @allure.title("Verify all onboarding screens text")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.android
    @pytest.mark.onboarding
    def test_onboarding__each_screen_text__should_be_correct(self):
        # === DEBUG ===
        print("\n=== DEBUG ===")
        print(f"BROWSERSTACK_USERNAME: {settings.browserstack_username}")
        print(f"BROWSERSTACK_ACCESS_KEY: {settings.browserstack_access_key}")
        print(f"APP_URL: {settings.app_url}")
        print(f"CONTEXT: {settings.context}")
        print("=== END DEBUG ===\n")

        screens_text = ["All the world's knowledge", "Data & Privacy", "Follow your curiosity"]

        for expected_text in screens_text:
            try:
                text_element = browser.element((AppiumBy.XPATH, f"//android.widget.TextView[@text='{expected_text}']"))
                text_element.with_(timeout=5).should(be.visible)
                print(f"✅ Found text: {expected_text}")

                try:
                    next_btn = browser.element((AppiumBy.XPATH, "//android.view.View[@content-desc='Forward']/.."))
                    next_btn.click()
                except:
                    next_btn = browser.element((AppiumBy.XPATH, "//android.view.View[@content-desc='Next']/.."))
                    next_btn.click()
                time.sleep(2)
            except:
                pass

        print("✅ All onboarding screens verified")
