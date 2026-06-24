import time

import allure
import pytest
from jsonschema import validate

from api.auth_client import auth_client
from api.products_client import products_client
from api.schemas import (
    login_response_schema,
    products_response_schema,
    signup_response_schema,
)


@allure.feature("API Tests")
@allure.story("Demoblaze API")
@pytest.mark.api
class TestDemoblazeAPI:
    @allure.title("POST /signup - регистрация нового пользователя")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_signup_new_user(self):
        username = f"testuser_{int(time.time())}"
        password = "password123"

        response = auth_client.signup(username, password)
        assert response.status_code == 200

        # Успешная регистрация возвращает пустую строку
        if response.text:
            validate(response.json(), signup_response_schema)

        # Проверяем, что пользователь может залогиниться
        login_response = auth_client.login(username, password)
        assert login_response.status_code == 200

        data = login_response.json()

        if isinstance(data, dict):
            assert data.get("errorMessage") is None, f"Login failed: {data.get('errorMessage')}"
        else:
            assert isinstance(data, str), f"Unexpected response type: {type(data)}"
            assert data == "" or "Auth_token" in data

    @allure.title("POST /signup - регистрация существующего пользователя")
    @allure.severity(allure.severity_level.NORMAL)
    def test_signup_existing_user(self):
        username = f"existing_{int(time.time())}"
        password = "password123"

        response1 = auth_client.signup(username, password)
        assert response1.status_code == 200

        response2 = auth_client.signup(username, password)
        assert response2.status_code == 200

        data = response2.json()
        validate(data, signup_response_schema)
        assert "errorMessage" in data
        assert "exist" in data["errorMessage"].lower()

    @allure.title("POST /bycat - получение товаров категории Phones")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_products_by_category_phones(self):
        response = products_client.get_by_category("phone")

        assert response.status_code == 200
        data = response.json()
        validate(data, products_response_schema)

        items = data.get("Items", [])
        assert len(items) > 0

        samsung = next((item for item in items if "Samsung" in item["title"]), None)
        assert samsung is not None, "Samsung phone not found in category Phones"
        assert samsung["price"] > 0

    @allure.title("POST /bycat - получение товаров категории Laptops")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_products_by_category_laptops(self):
        response = products_client.get_by_category("notebook")

        assert response.status_code == 200
        data = response.json()
        validate(data, products_response_schema)

        items = data.get("Items", [])
        assert len(items) > 0

        sony = next((item for item in items if "Sony" in item["title"]), None)
        assert sony is not None, "Sony laptop not found in category Laptops"
        assert sony["price"] > 0

    @allure.title("POST /login - авторизация с неверным паролем")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_wrong_password(self):
        username = f"login_test_{int(time.time())}"
        password = "correctpassword"

        auth_client.signup(username, password)

        response = auth_client.login(username, "wrongpassword")
        assert response.status_code == 200

        data = response.json()
        validate(data, login_response_schema)
        assert "Wrong password" in data["errorMessage"]

    @allure.title("POST /login - авторизация несуществующего пользователя")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_nonexistent_user(self):
        response = auth_client.login("nonexistent_user_xyz", "password123")

        assert response.status_code == 200

        data = response.json()
        validate(data, login_response_schema)
        assert "User does not exist" in data["errorMessage"]
