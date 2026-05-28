from __future__ import annotations

import allure
import pytest

from pages.wikipedia_app import wikipedia


@allure.suite("Wikipedia Mobile Tests")
@allure.tag("android", "article", "bstack")
@allure.title("Article viewing functionality tests")
class TestWikipediaArticle:

    @allure.title("Search and click on article result")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("""
    Test objective: Verify that user can open an article from search results.

    Steps:
    1. Close onboarding if present
    2. Search for query 'Selenium WebDriver'
    3. Verify search results contain 'Selenium'
    4. Click on first search result
    5. Verify article page is opened
    """)
    @pytest.mark.android
    @pytest.mark.article
    @pytest.mark.bstack
    def test_article_click__search_and_click_result__should_open_article(self):
        # Given: Wikipedia app is open
        wikipedia.close_onboarding_if_present()

        # When: User searches for "Selenium WebDriver"
        wikipedia.search("Selenium WebDriver")

        # Then: Search results should contain "Selenium"
        wikipedia.results_should_contain_text("Selenium")

        # When: User clicks on first result
        wikipedia.click_first_result()

        # Then: Article page should be opened
        wikipedia.article_should_be_opened()

    @allure.title("Search and click on specific article by text")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("""
    Test objective: Verify that user can open a specific article.

    Steps:
    1. Search for query 'Python'
    2. Click on result containing 'Python (programming language)'
    3. Verify article title contains 'Python'
    """)
    @pytest.mark.android
    @pytest.mark.article
    def test_article_click__search_and_click_specific_article__should_open_correct_article(self):
        # Given: Wikipedia app is open
        wikipedia.close_onboarding_if_present()

        # When: User searches for "Python programming"
        wikipedia.search("Python programming")

        # Then: Search results should contain "Python"
        wikipedia.results_should_contain_text("Python")

        # When: User clicks on result containing specific text
        wikipedia.click_result_containing_text("Python")

        # Then: Article should contain expected text
        wikipedia.article_title_should_contain("Python")

    @allure.title("Open article and navigate back")
    @allure.severity(allure.severity_level.MINOR)
    @allure.description("""
    Test objective: Verify navigation back from article to search results.

    Steps:
    1. Search for query 'Automation'
    2. Click on first search result
    3. Verify article is opened
    4. Go back
    5. Verify search results are still visible
    """)
    @pytest.mark.android
    @pytest.mark.article
    def test_article_click__open_article_and_go_back__should_return_to_search_results(self):
        # Given: Wikipedia app is open
        wikipedia.close_onboarding_if_present()

        # When: User searches and opens an article
        wikipedia.search("Automation testing")
        wikipedia.results_should_have_count_greater_than(0)
        wikipedia.click_first_result()
        wikipedia.article_should_be_opened()

        # When: User goes back
        wikipedia.go_back()

        # Then: Should return to search results
        import time
        time.sleep(2)

        # Verify search results are still visible
        wikipedia.results_should_have_count_greater_than(0)

        allure.attach(
            "Successfully navigated back to search results",
            name="Navigation result",
            attachment_type=allure.attachment_type.TEXT
        )