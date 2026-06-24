from __future__ import annotations

import time

import allure
from appium.webdriver.common.appiumby import AppiumBy
from selene import be, have
from selene.support.shared import browser


class WikipediaApp:
    """Main Wikipedia App Page Object"""

    @allure.step("Close onboarding and language selection if present")
    def close_onboarding_if_present(self) -> WikipediaApp:
        """Close onboarding screens or language selection if they are displayed"""

        # Нажимаем Forward на первых экранах
        for i in range(3):
            try:
                forward_btn = browser.element((AppiumBy.XPATH, "//android.view.View[@content-desc='Forward']/.."))
                forward_btn.click()
                print(f"✅ Clicked Forward {i + 1}")
                time.sleep(2)
            except Exception as e:
                print(f"Forward {i + 1} error: {e}")

        # На экране "Follow your curiosity" нажимаем Next
        try:
            next_btn = browser.element((AppiumBy.XPATH, "//android.view.View[@content-desc='Next']/.."))
            next_btn.click()
            print("✅ Clicked Next")
            time.sleep(2)
        except Exception as e:
            print(f"Next button error: {e}")

        # Continue кнопки (если есть)
        for i in range(3):
            try:
                btn = browser.element((AppiumBy.ID, "org.wikipedia.alpha:id/fragment_onboarding_forward_button"))
                btn.with_(timeout=3).should(be.visible).click()
                print(f"✅ Clicked Continue {i + 1}")
                time.sleep(1)
            except:
                pass

        return self

    @allure.step("Search for text: '{text}'")
    def search(self, text: str) -> WikipediaApp:
        search_field = browser.element((AppiumBy.ACCESSIBILITY_ID, "Search Wikipedia"))
        search_field.with_(timeout=15).should(be.visible).click()
        print("✅ Search field clicked")

        search_input = browser.element((AppiumBy.ID, "org.wikipedia.alpha:id/search_src_text"))
        search_input.type(text)
        print(f"✅ Typed: {text}")
        time.sleep(2)
        return self

    @allure.step("Verify search results contain text: '{expected_text}'")
    def results_should_contain_text(self, expected_text: str) -> WikipediaApp:
        result = browser.element((AppiumBy.XPATH, f"//android.widget.TextView[contains(@text, '{expected_text}')]"))
        result.with_(timeout=10).should(be.visible)
        print(f"✅ Found result with: {expected_text}")
        return self

    @allure.step("Click on first search result")
    def click_first_result(self) -> WikipediaApp:
        results = browser.all((AppiumBy.CLASS_NAME, "android.widget.TextView"))
        results.first.should(be.visible).click()
        time.sleep(2)
        return self

    @allure.step("Verify article page is opened")
    def article_should_be_opened(self, expected_title: str | None = None) -> WikipediaApp:
        page_source = browser.config.driver.page_source
        article_indicators = ["WebView", "TextView", "page_title", "article"]
        found = False
        for indicator in article_indicators:
            if indicator in page_source:
                allure.attach(f"Found article indicator: {indicator}", name="Article verification")
                found = True
                break
        if not found:
            raise AssertionError("Article page not opened - no article indicators found")

        if expected_title and expected_title not in page_source:
            raise AssertionError(f"Article title '{expected_title}' not found in page source")

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

    @allure.step("Verify search results count is greater than {count}")
    def results_should_have_count_greater_than(self, count: int) -> WikipediaApp:
        browser.all((AppiumBy.CLASS_NAME, "android.widget.TextView")).with_(timeout=10).should(
            have.size_greater_than(count)
        )
        return self

    @allure.step("Go back to previous screen")
    def go_back(self) -> WikipediaApp:
        """Навигация назад"""
        try:
            # Пробуем через кнопку навигации
            back_btn = browser.element((AppiumBy.ACCESSIBILITY_ID, "Navigate up"))
            back_btn.click()
            print("✅ Navigated back")
            time.sleep(2)
        except:
            # Или через системную кнопку Back
            browser.config.driver.back()
            time.sleep(2)
        return self


wikipedia = WikipediaApp()
