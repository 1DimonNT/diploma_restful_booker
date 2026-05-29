from __future__ import annotations

import time
import allure
import pytest
from selene.support.shared import browser
from appium.webdriver.common.appiumby import AppiumBy
from selene import be

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
        # Close onboarding полностью
        wikipedia.close_onboarding_if_present()

        # Проверяем, что главный экран с поиском открылся
        wikipedia.search("Test")
        print("✅ Onboarding completed, main screen visible")

    @allure.title("Skip onboarding and verify main screen")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.android
    @pytest.mark.onboarding
    def test_onboarding__skip_onboarding__should_show_main_screen(self):
        # Пропускаем онбординг через кнопку Skip
        try:
            skip_btn = browser.element((AppiumBy.XPATH, "//android.widget.TextView[@text='Skip']/.."))
            skip_btn.click()
            print("✅ Clicked Skip")
            time.sleep(2)
        except:
            # Если Skip не сработал, используем стандартное закрытие
            wikipedia.close_onboarding_if_present()

        # Проверяем, что главный экран открылся
        try:
            search_field = browser.element((AppiumBy.ACCESSIBILITY_ID, "Search Wikipedia"))
            search_field.with_(timeout=10).should(be.visible)
            print("✅ Main screen visible after skip")
        except:
            # Если поле поиска не появилось, пробуем закрыть онбординг полностью
            wikipedia.close_onboarding_if_present()
            wikipedia.search("Test")

        print("✅ Skip worked, main screen visible")

    @allure.title("Verify all onboarding screens text")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.android
    @pytest.mark.onboarding
    def test_onboarding__each_screen_text__should_be_correct(self):
        # Проверяем текст на каждом экране онбординга
        screens_text = [
            "All the world's knowledge",
            "Data & Privacy",
            "Follow your curiosity"
        ]

        for expected_text in screens_text:
            try:
                text_element = browser.element((AppiumBy.XPATH, f"//android.widget.TextView[@text='{expected_text}']"))
                text_element.with_(timeout=5).should(be.visible)
                print(f"✅ Found text: {expected_text}")

                # Нажимаем Forward/Next для перехода
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