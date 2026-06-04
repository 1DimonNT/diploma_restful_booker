from __future__ import annotations

import allure
import pytest

from mobile.pages.wikipedia_app import wikipedia


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
        wikipedia.close_onboarding_if_present()
        wikipedia.search("BrowserStack")
        wikipedia.results_should_contain_text("BrowserStack")
