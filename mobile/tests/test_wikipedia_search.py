from __future__ import annotations

import time
import allure
import pytest
from selene.support.shared import browser
from appium.webdriver.common.appiumby import AppiumBy
from selene import be

from pages.wikipedia_app import wikipedia


@allure.suite("Wikipedia Mobile Tests")
@allure.tag("android", "search", "bstack")
@allure.title("Search functionality tests")
class TestWikipediaSearch:

    @allure.title("Search for 'BrowserStack' and verify results exist")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.android
    @pytest.mark.search
    @pytest.mark.bstack
    def test_search_in_wikipedia__valid_query_BrowserStack__should_find_results(self):
        # Close onboarding
        try:
            for i in range(3):
                btn = browser.element((AppiumBy.ID, "org.wikipedia.alpha:id/fragment_onboarding_forward_button"))
                btn.with_(timeout=5).should(be.visible).click()
                time.sleep(1)
        except:
            pass

        # Click GET STARTED
        try:
            get_started = browser.element((AppiumBy.XPATH,
                                           "//android.widget.Button[contains(@text, 'GET STARTED') or contains(@text, 'Get started')]"))
            get_started.click()
            time.sleep(2)
        except:
            pass

        # Close banner
        try:
            close_icon = browser.element((AppiumBy.XPATH, "//android.view.View[@content-desc='Close']/.."))
            close_icon.click()
            time.sleep(2)
        except:
            pass

        # Search
        wikipedia.search("BrowserStack")
        wikipedia.results_should_contain_text("BrowserStack")