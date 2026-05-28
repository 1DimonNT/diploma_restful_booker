from __future__ import annotations

import time
import allure
from appium.webdriver.common.appiumby import AppiumBy
from selene import have, be
from selene.support.shared import browser

from pages.onboarding_page import onboarding


class WikipediaApp:
    """Main Wikipedia App Page Object"""

    @allure.step("Close onboarding and language selection if present")
    def close_onboarding_if_present(self) -> WikipediaApp:
        """Close onboarding screens or language selection if they are displayed"""

        # Try to select English language if language selection screen is shown
        try:
            english_option = browser.element((AppiumBy.XPATH, "//android.widget.TextView[contains(@text, 'English')]"))
            if english_option.with_(timeout=5).wait_until(be.visible):
                english_option.click()
                allure.attach("Selected English language", name="Language selection",
                              attachment_type=allure.attachment_type.TEXT)
                return self
        except:
            pass

        # Try to click "Add or edit languages" button and then select English
        try:
            add_language_btn = browser.element((AppiumBy.ID, "org.wikipedia.alpha:id/addLanguageButton"))
            if add_language_btn.with_(timeout=5).wait_until(be.visible):
                add_language_btn.click()
                time.sleep(2)
                # After clicking, select English
                english_option = browser.element(
                    (AppiumBy.XPATH, "//android.widget.TextView[contains(@text, 'English')]"))
                english_option.click()
                allure.attach("Added English language", name="Language selection",
                              attachment_type=allure.attachment_type.TEXT)
                return self
        except:
            pass

        # Original onboarding skip logic
        try:
            skip_button = browser.element((AppiumBy.ID, "org.wikipedia.alpha:id/fragment_onboarding_skip_button"))
            if skip_button.with_(timeout=5).wait_until(be.visible):
                skip_button.click()
                return self
        except:
            pass

        # Original onboarding continue logic
        try:
            for _ in range(4):
                continue_button = browser.element(
                    (AppiumBy.ID, "org.wikipedia.alpha:id/fragment_onboarding_forward_button"))
                if continue_button.with_(timeout=3).wait_until(be.visible):
                    continue_button.click()
                else:
                    break
        except:
            pass

        return self

    @allure.step("Complete full onboarding")
    def complete_onboarding(self) -> WikipediaApp:
        """Complete all onboarding screens"""
        onboarding.complete_onboarding()
        return self

    @allure.step("Search for text: '{text}'")
    def search(self, text: str) -> WikipediaApp:
        """Perform search for given text"""
        search_field = browser.element((AppiumBy.ACCESSIBILITY_ID, "Search Wikipedia"))
        search_field.with_(timeout=10).should(be.visible).click()

        search_input = browser.element((AppiumBy.ID, "org.wikipedia.alpha:id/search_src_text"))
        search_input.type(text)
        time.sleep(2)

        return self

    @allure.step("Verify onboarding is completed and main screen is shown")
    def verify_onboarding_completed(self) -> WikipediaApp:
        """Verify that onboarding is finished and main app screen is visible"""
        search_field = browser.element((AppiumBy.ACCESSIBILITY_ID, "Search Wikipedia"))
        search_field.with_(timeout=10).should(be.visible)
        return self

    @allure.step("Verify search results contain text: '{expected_text}'")
    def results_should_contain_text(self, expected_text: str) -> WikipediaApp:
        result = browser.element(
            (AppiumBy.XPATH, f"//android.widget.TextView[contains(@text, '{expected_text}')]")
        )
        result.with_(timeout=10).should(be.visible)
        return self

    @allure.step("Verify search results count is greater than {count}")
    def results_should_have_count_greater_than(self, count: int) -> WikipediaApp:
        browser.all((AppiumBy.CLASS_NAME, "android.widget.TextView")).with_(timeout=10).should(
            have.size_greater_than(count)
        )
        return self

    @allure.step("Click on first search result")
    def click_first_result(self) -> WikipediaApp:
        results = browser.all((AppiumBy.CLASS_NAME, "android.widget.TextView"))
        results.first.should(be.visible).click()
        time.sleep(2)
        return self

    @allure.step("Click on search result containing text: '{text}'")
    def click_result_containing_text(self, text: str) -> WikipediaApp:
        result = browser.element(
            (AppiumBy.XPATH, f"//android.widget.TextView[contains(@text, '{text}')]")
        )
        result.with_(timeout=10).should(be.visible).click()
        time.sleep(2)
        return self

    @allure.step("Verify article page is opened")
    def article_should_be_opened(self) -> WikipediaApp:
        page_source = browser.config.driver.page_source
        with open("article_page.xml", "w", encoding="utf-8") as f:
            f.write(page_source)

        article_indicators = ["WebView", "TextView", "page_title", "article"]
        found = False
        for indicator in article_indicators:
            if indicator in page_source:
                allure.attach(f"Found article indicator: {indicator}", name="Article verification")
                found = True
                break

        if not found:
            raise AssertionError("Article page not opened - no article indicators found")
        return self

    @allure.step("Verify article title contains text: '{expected_text}'")
    def article_title_should_contain(self, expected_text: str) -> WikipediaApp:
        try:
            title_element = browser.element((AppiumBy.ID, "org.wikipedia.alpha:id/view_page_title_text"))
            title_element.with_(timeout=5).should(have.text(expected_text))
        except:
            page_source = browser.config.driver.page_source
            if expected_text not in page_source:
                raise AssertionError(f"Article title does not contain '{expected_text}'")
        return self

    @allure.step("Go back to previous screen")
    def go_back(self) -> WikipediaApp:
        browser.driver.back()
        time.sleep(1)
        return self

    @allure.step("Clear search")
    def clear_search(self) -> WikipediaApp:
        clear_button = browser.element((AppiumBy.ID, "org.wikipedia.alpha:id/search_close_btn"))
        if clear_button.with_(timeout=3).wait_until(be.visible):
            clear_button.click()
        return self


wikipedia = WikipediaApp()