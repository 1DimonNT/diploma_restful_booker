import allure
import pytest
import requests
from jsonschema import validate
from config import settings

BASE_URL = settings.API_BASE_URL

# Schema для списка товаров
products_schema = {
    "type": "object",
    "properties": {
        "Items": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "title": {"type": "string"},
                    "price": {"type": "integer"}
                },
                "required": ["id", "title", "price"]
            }
        }
    },
    "required": ["Items"]
}

# Schema для одного товара
product_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "title": {"type": "string"},
        "price": {"type": "integer"}
    },
    "required": ["id", "title", "price"]
}

# Schema для ошибки
error_schema = {
    "type": "object",
    "properties": {
        "errorMessage": {"type": "string"}
    },
    "required": ["errorMessage"]
}


@allure.feature("API Tests")
@allure.story("Demoblaze API")
@pytest.mark.api
class TestDemoblazeAPI:

    @allure.title("GET /entries - получение всех товаров")
    def test_get_all_products(self):
        with allure.step("Выполнить GET запрос"):
            response = requests.get(f"{BASE_URL}/entries")

        with allure.step("Проверить статус 200"):
            assert response.status_code == 200

        with allure.step("Проверить схему ответа"):
            validate(response.json(), products_schema)

        with allure.step("Проверить что список не пуст"):
            assert len(response.json()["Items"]) > 0

    @allure.title("POST /view - получение товара по ID")
    def test_get_product_by_id(self):
        with allure.step("Выполнить POST запрос"):
            response = requests.post(f"{BASE_URL}/view", json={"id": 1})

        with allure.step("Проверить статус 200"):
            assert response.status_code == 200

        with allure.step("Проверить схему ответа"):
            validate(response.json(), product_schema)

        with allure.step("Проверить данные товара"):
            assert response.json()["title"] == "Samsung galaxy s6"

    @allure.title("POST /bycat - товары категории Phones")
    def test_get_products_by_category_phones(self):
        response = requests.post(f"{BASE_URL}/bycat", json={"cat": "phone"})
        assert response.status_code == 200
        validate(response.json(), products_schema)
        assert len(response.json()["Items"]) > 0

    @allure.title("POST /bycat - товары категории Laptops")
    def test_get_products_by_category_laptops(self):
        response = requests.post(f"{BASE_URL}/bycat", json={"cat": "notebook"})
        assert response.status_code == 200
        validate(response.json(), products_schema)
        items = response.json()["Items"]
        assert any("Sony" in item["title"] for item in items)

    @allure.title("POST /login - неверный пароль")
    def test_login_wrong_password(self):
        response = requests.post(f"{BASE_URL}/login", json={
            "username": "testuser",
            "password": "wrongpassword"
        })
        assert response.status_code == 200
        validate(response.json(), error_schema)
        assert "Wrong password" in response.json()["errorMessage"]

    @allure.title("POST /login - несуществующий пользователь")
    def test_login_nonexistent_user(self):
        response = requests.post(f"{BASE_URL}/login", json={
            "username": "nonexistent_12345",
            "password": "test"
        })
        assert response.status_code == 200
        assert response.json()["errorMessage"] == "User does not exist."