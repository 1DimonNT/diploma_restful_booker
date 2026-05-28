from __future__ import annotations

import allure
from appium.webdriver.common.appiumby import AppiumBy
from selene import have, be
from selene.support.shared import browser


class OnboardingPage:
    """Page Object for Wikipedia onboarding screens"""

    def __init__(self):
        # Onboarding screen elements
        self.primary_text = browser.element((AppiumBy.ID, "org.wikipedia.alpha:id/primaryText"))
        self.secondary_text = browser.element((AppiumBy.ID, "org.wikipedia.alpha:id/secondaryText"))
        self.continue_button = browser.element(
            (AppiumBy.ID, "org.wikipedia.alpha:id/fragment_onboarding_forward_button"))
        self.skip_button = browser.element((AppiumBy.ID, "org.wikipedia.alpha:id/fragment_onboarding_skip_button"))

        # Screen titles for verification
        self.screen_titles = [
            "The Free Encyclopedia",
            "Over 40 million articles",
            "Create your account",
            "Help improve Wikipedia"
        ]

        # Screen descriptions
        self.screen_descriptions = [
            "The Wikipedia app is the official app for the world's largest encyclopedia.",
            "Access articles from around the world, all in one place.",
            "Sync your reading lists across devices and contribute to the community.",
            "Join millions of readers and contributors worldwide."
        ]

    @allure.step("Wait for onboarding screen to load")
    def wait_for_loading(self) -> OnboardingPage:
        """Wait for onboarding screen to be fully loaded"""
        self.primary_text.with_(timeout=10).should(be.visible)
        return self

    @allure.step("Verify onboarding screen text - Screen {screen_number}")
    def verify_screen_text(self, screen_number: int) -> OnboardingPage:
        """Verify title and description for specific onboarding screen"""
        # Screen numbers are 1-indexed for readability (1-4)
        index = screen_number - 1

        expected_title = self.screen_titles[index]
        expected_description = self.screen_descriptions[index]

        # Verify title
        self.primary_text.should(have.text(expected_title))

        # Verify description (may not be present on all screens)
        if expected_description:
            self.secondary_text.should(have.text(expected_description))

        allure.attach(
            f"Screen {screen_number}: {expected_title}",
            name="Onboarding screen verified",
            attachment_type=allure.attachment_type.TEXT
        )

        return self

    @allure.step("Click continue button")
    def click_continue(self) -> OnboardingPage:
        """Click continue button to go to next screen"""
        self.continue_button.should(be.visible).click()
        return self

    @allure.step("Click skip button")
    def click_skip(self) -> OnboardingPage:
        """Click skip button to close onboarding"""
        self.skip_button.should(be.visible).click()
        return self

    @allure.step("Complete full onboarding flow")
    def complete_onboarding(self) -> OnboardingPage:
        """Complete all 4 onboarding screens"""
        for screen in range(1, 5):  # Screens 1 through 4
            self.wait_for_loading()
            self.verify_screen_text(screen)

            # On last screen, the button might change to "Get started" or similar
            if screen < 4:
                self.click_continue()
            else:
                # Last screen - click button to finish
                self.click_continue()

        return self

    @allure.step("Verify onboarding is completed and main screen is shown")
    def verify_onboarding_completed(self) -> OnboardingPage:
        """Verify that onboarding is finished and main app screen is visible"""
        # After onboarding, search field should be visible
        search_field = browser.element((AppiumBy.ACCESSIBILITY_ID, "Search Wikipedia"))
        search_field.with_(timeout=10).should(be.visible)

        allure.attach(
            "Onboarding completed successfully, main screen is visible",
            name="Onboarding status",
            attachment_type=allure.attachment_type.TEXT
        )

        return self

    @allure.step("Check if onboarding is displayed")
    def is_onboarding_displayed(self) -> bool:
        """Check if onboarding screen is currently displayed"""
        try:
            self.primary_text.with_(timeout=3).should(be.visible)
            return True
        except:
            return False


# Singleton instance for easy import
onboarding = OnboardingPage()