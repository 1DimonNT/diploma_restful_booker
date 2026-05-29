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

        assert response.is_success, f"Registration failed: {response.errorMessage}"

    @allure.title("POST /signup - регистрация существующего пользователя")
    @allure.severity(allure.severity_level.NORMAL)
    def test_signup_existing_user(self):
        username = f"existing_{int(time.time())}"
        # Первая регистрация
        api_client.signup(username, "password123")
        # Вторая регистрация (должна упасть)
        response = api_client.signup(username, "password123")

        assert response.errorMessage is not None
        assert "exist" in response.errorMessage.lower()

    @allure.title("POST /bycat - получение товаров категории Phones")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_products_by_category_phones(self):
        response = api_client.get_products_by_category("phone")

        assert response.count > 0, "No products found in Phones category"

    @allure.title("POST /bycat - получение товаров категории Laptops")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_products_by_category_laptops(self):
        response = api_client.get_products_by_category("notebook")

        assert response.count > 0, "No products found in Laptops category"

    @allure.title("POST /login - авторизация с неверным паролем (существующий пользователь)")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_wrong_password(self):
        # Сначала создаем пользователя
        username = f"login_test_{int(time.time())}"
        api_client.signup(username, "correctpassword")

        # Пробуем войти с неверным паролем
        response = api_client.login(username, "wrongpassword")

        assert "Wrong password" in response.errorMessage

    @allure.title("POST /login - авторизация несуществующего пользователя")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_nonexistent_user(self):
        response = api_client.login("nonexistent_user_xyz", "password123")

        assert "User does not exist" in response.errorMessage