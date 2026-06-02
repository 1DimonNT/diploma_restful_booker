import allure
import pytest
import time
from api.client import api_client


@allure.feature("API Tests")
@allure.story("Demoblaze API")
@pytest.mark.api
class TestDemoblazeAPI:

    @allure.title("POST /signup - регистрация нового пользователя")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_signup_new_user(self):
        unique_username = f"testuser_{int(time.time())}"
        response = api_client.signup(unique_username, "password123")

        # Успешная регистрация возвращает пустую строку или {"errorMessage": null}
        assert response == "" or response.get("errorMessage") is None

    @allure.title("POST /signup - регистрация существующего пользователя")
    @allure.severity(allure.severity_level.NORMAL)
    def test_signup_existing_user(self):
        username = f"existing_{int(time.time())}"
        # Первая регистрация
        api_client.signup(username, "password123")
        # Вторая регистрация (должна вернуть ошибку)
        response = api_client.signup(username, "password123")

        assert "errorMessage" in response
        assert "exist" in response["errorMessage"].lower()

    @allure.title("POST /bycat - получение товаров категории Phones")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_products_by_category_phones(self):
        response = api_client.get_products_by_category("phone")

        assert len(response.get("Items", [])) > 0

    @allure.title("POST /bycat - получение товаров категории Laptops")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_products_by_category_laptops(self):
        response = api_client.get_products_by_category("notebook")

        assert len(response.get("Items", [])) > 0

    @allure.title("POST /login - авторизация с неверным паролем")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_wrong_password(self):
        username = f"login_test_{int(time.time())}"
        api_client.signup(username, "correctpassword")

        response = api_client.login(username, "wrongpassword")

        assert "Wrong password" in response["errorMessage"]

    @allure.title("POST /login - авторизация несуществующего пользователя")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_nonexistent_user(self):
        response = api_client.login("nonexistent_user_xyz", "password123")

        assert "User does not exist" in response["errorMessage"]