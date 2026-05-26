import allure
import pytest
from jsonschema import validate
from api.client import api_client
from api.schemas.product import products_response_schema, product_schema, error_schema


@allure.epic("API Testing")
@allure.feature("Demoblaze API")
@allure.story("Products and Authentication")
@pytest.mark.api
class TestDemoblazeAPI:

    @allure.title("GET /entries - получение списка всех товаров")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("positive", "smoke")
    def test_get_all_products(self):
        with allure.step("Выполнить GET запрос к /entries"):
            response = api_client.get("/entries")

        with allure.step("Проверить статус код 200"):
            assert response.status_code == 200

        with allure.step("Проверить схему ответа"):
            validate(response.json(), products_response_schema)

        with allure.step("Проверить, что список товаров не пуст"):
            assert len(response.json()["Items"]) > 0

    @allure.title("POST /view - получение товара по ID")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("positive")
    def test_post_get_product_by_id(self):
        with allure.step("Выполнить POST запрос к /view с id=1"):
            response = api_client.post("/view", data={"id": 1})

        with allure.step("Проверить статус код 200"):
            assert response.status_code == 200

        with allure.step("Проверить схему ответа"):
            validate(response.json(), product_schema)

        with allure.step("Проверить данные товара"):
            product = response.json()
            assert product["title"] == "Samsung galaxy s6"
            assert product["price"] == 360

    @allure.title("POST /bycat - получение товаров по категории Phones")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("positive")
    def test_post_get_products_by_category_phones(self):
        with allure.step("Выполнить POST запрос к /bycat с cat=phone"):
            response = api_client.post("/bycat", data={"cat": "phone"})

        with allure.step("Проверить статус код 200"):
            assert response.status_code == 200

        with allure.step("Проверить схему ответа"):
            validate(response.json(), products_response_schema)

        with allure.step("Проверить, что товары из категории Phones"):
            items = response.json()["Items"]
            assert len(items) > 0

    @allure.title("POST /bycat - получение товаров по категории Laptops")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("positive")
    def test_post_get_products_by_category_laptops(self):
        with allure.step("Выполнить POST запрос к /bycat с cat=notebook"):
            response = api_client.post("/bycat", data={"cat": "notebook"})

        with allure.step("Проверить статус код 200"):
            assert response.status_code == 200

        with allure.step("Проверить схему ответа"):
            validate(response.json(), products_response_schema)

        with allure.step("Проверить наличие товаров Sony"):
            items = response.json()["Items"]
            assert any("Sony" in item["title"] for item in items)

    @allure.title("POST /login - попытка входа с неверным паролем")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("negative")
    def test_post_login_wrong_password(self):
        with allure.step("Выполнить POST запрос к /login с неверным паролем"):
            response = api_client.post("/login", data={
                "username": "testuser",
                "password": "wrongpassword"
            })

        with allure.step("Проверить статус код 200"):
            assert response.status_code == 200

        with allure.step("Проверить схему ответа с ошибкой"):
            validate(response.json(), error_schema)

        with allure.step("Проверить сообщение об ошибке"):
            assert "Wrong password" in response.json()["errorMessage"]

    @allure.title("POST /login - попытка входа с несуществующим пользователем")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("negative")
    def test_post_login_nonexistent_user(self):
        with allure.step("Выполнить POST запрос к /login с несуществующим пользователем"):
            response = api_client.post("/login", data={
                "username": "nonexistent_user_12345",
                "password": "test"
            })

        with allure.step("Проверить статус код 200"):
            assert response.status_code == 200

        with allure.step("Проверить сообщение об ошибке"):
            assert response.json()["errorMessage"] == "User does not exist."