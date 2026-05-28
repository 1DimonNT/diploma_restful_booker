from __future__ import annotations

import allure
import pytest

from pages.wikipedia_app import wikipedia


@allure.suite("Wikipedia Mobile Tests")
@allure.tag("android", "onboarding", "local")
@allure.title("Onboarding screens should work correctly")
class TestOnboarding:

    @allure.title("Complete onboarding flow and verify main screen")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("""
    Test objective: Verify that the onboarding screens work correctly.

    Steps:
    1. Complete all 4 onboarding screens
    2. Verify each screen displays correct text
    3. Verify that after completion, main app screen is shown
    """)
    @pytest.mark.android
    @pytest.mark.onboarding
    def test_onboarding__complete_flow__should_show_main_screen(self):
        # Given: Wikipedia app is opened for the first time
        # When: User completes all onboarding screens
        wikipedia.complete_onboarding()

        # Then: Main app screen should be visible
        wikipedia.verify_onboarding_completed()

    @allure.title("Skip onboarding and verify main screen")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("""
    Test objective: Verify that user can skip onboarding.

    Steps:
    1. When onboarding appears, click Skip
    2. Verify that main app screen is shown immediately
    """)
    @pytest.mark.android
    @pytest.mark.onboarding
    def test_onboarding__skip_onboarding__should_show_main_screen(self):
        # Given: Wikipedia app is opened for the first time
        # When: User skips onboarding
        wikipedia.close_onboarding_if_present()

        # Then: Main app screen should be visible
        wikipedia.verify_onboarding_completed()

    @allure.title("Verify each onboarding screen text")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("""
    Test objective: Verify that each onboarding screen displays correct text.

    Steps:
    1. Navigate through each onboarding screen
    2. Verify title and description for each screen
    3. Ensure text matches expected values
    """)
    @pytest.mark.android
    @pytest.mark.onboarding
    def test_onboarding__each_screen_text__should_be_correct(self):
        from pages.onboarding_page import onboarding

        # Screen 1 - The Free Encyclopedia
        onboarding.wait_for_loading()
        onboarding.verify_screen_text(1)
        onboarding.click_continue()

        # Screen 2 - Over 40 million articles
        onboarding.wait_for_loading()
        onboarding.verify_screen_text(2)
        onboarding.click_continue()

        # Screen 3 - Create your account
        onboarding.wait_for_loading()
        onboarding.verify_screen_text(3)
        onboarding.click_continue()

        # Screen 4 - Help improve Wikipedia
        onboarding.wait_for_loading()
        onboarding.verify_screen_text(4)
        onboarding.click_continue()

        # Verify onboarding is complete
        onboarding.verify_onboarding_completed()