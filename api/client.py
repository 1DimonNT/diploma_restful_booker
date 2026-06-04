"""API клиент для Demoblaze с JSON Schema валидацией"""

import json

import allure
import requests
from jsonschema import validate

from api.schemas import login_response_schema, product_response_schema, products_response_schema, signup_response_schema
from config import settings
from utils.logger import log


class ApiClient:
    def __init__(self):
        self.base_url = settings.API_BASE_URL
        self.timeout = settings.API_TIMEOUT
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})

    def _request(self, method: str, endpoint: str, json_data: dict | None = None, schema: dict | None = None):
        """Выполняет запрос с валидацией через JSON Schema"""
        url = f"{self.base_url}{endpoint}"

        with allure.step(f"API {method} {endpoint}"):
            log.info(f"📤 {method} {url}")
            if json_data:
                log.debug(f"Request body: {json_data}")
                allure.attach(json.dumps(json_data, indent=2), "Request Body", allure.attachment_type.JSON)

            response = self.session.request(method=method, url=url, json=json_data, timeout=self.timeout)

            log.info(f"📥 Response: {response.status_code}")

            # Если ответ пустой, возвращаем пустую строку
            if response.text == "":
                allure.attach("Empty response body", "Response Body", allure.attachment_type.TEXT)
                if schema:
                    validate(instance="", schema=schema)
                    log.info("✅ JSON Schema validation passed")
                return ""

            # Парсим JSON ответ
            response_data = response.json()
            allure.attach(
                json.dumps(response_data, indent=2, ensure_ascii=False), "Response Body", allure.attachment_type.JSON
            )

            if schema:
                validate(instance=response_data, schema=schema)
                log.info("✅ JSON Schema validation passed")

            return response_data

    def signup(self, username: str, password: str):
        """Регистрация нового пользователя"""
        json_data = {"username": username, "password": password}
        return self._request("POST", "/signup", json_data, signup_response_schema)

    def login(self, username: str, password: str):
        """Авторизация пользователя"""
        json_data = {"username": username, "password": password}
        return self._request("POST", "/login", json_data, login_response_schema)

    def get_products_by_category(self, category: str):
        """Получение товаров по категории"""
        json_data = {"cat": category}
        return self._request("POST", "/bycat", json_data, products_response_schema)

    def get_product_by_id(self, product_id: int):
        """Получение товара по ID"""
        json_data = {"id": product_id}
        return self._request("POST", "/view", json_data, product_response_schema)


api_client = ApiClient()
