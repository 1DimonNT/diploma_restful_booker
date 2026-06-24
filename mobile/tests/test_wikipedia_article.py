from __future__ import annotations

import allure
import pytest

from mobile.pages.wikipedia_app import wikipedia


@allure.suite("Wikipedia Mobile Tests")
@allure.tag("android", "article", "bstack")
@allure.title("Article viewing functionality tests")
class TestWikipediaArticle:
    @allure.title("Search and click on article result")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.android
    @pytest.mark.article
    @pytest.mark.bstack
    def test_article_click__search_and_click_result__should_open_article(self):
        wikipedia.close_onboarding_if_present()
        wikipedia.search("Selenium WebDriver")
        wikipedia.results_should_contain_text("Selenium")
        wikipedia.click_first_result()
        wikipedia.article_should_be_opened()

    @allure.title("Search and click on specific article by text")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.android
    @pytest.mark.article
    def test_article_click__search_and_click_specific_article__should_open_correct_article(self):
        wikipedia.close_onboarding_if_present()
        wikipedia.search("Python (programming language)")
        wikipedia.results_should_contain_text("Python")
        wikipedia.click_first_result()
        wikipedia.article_should_be_opened()

    @allure.title("Open article and navigate back")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.android
    @pytest.mark.article
    def test_article_click__open_article_and_go_back__should_return_to_search_results(self):
        wikipedia.close_onboarding_if_present()
        wikipedia.search("Automation")
        wikipedia.results_should_contain_text("Automation")
        wikipedia.click_first_result()
        wikipedia.article_should_be_opened()
        wikipedia.go_back()
        wikipedia.results_should_contain_text("Automation")
        print("✅ Successfully navigated back to search results")
