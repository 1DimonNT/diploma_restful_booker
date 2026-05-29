"""API клиент для Demoblaze с Pydantic моделями"""
import allure
import requests
from typing import Optional, TypeVar, Generic, Type
from requests import Response
from config import settings
from utils.logger import log
from pydantic import BaseModel
from api.models import (
    SignupRequest, LoginRequest, ByCatRequest, ViewProductRequest,
    ProductsResponse, ProductResponse, ErrorResponse, SignupResponse
)

T = TypeVar('T')


class ApiClient:
    """Клиент для работы с Demoblaze API"""

    def __init__(self):
        self.base_url = settings.API_BASE_URL
        self.timeout = settings.API_TIMEOUT
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})

    def _request(
        self,
        method: str,
        endpoint: str,
        request_model: Optional[BaseModel] = None,
        response_model: Optional[Type[T]] = None,
        expected_status: int = 200
    ) -> T:
        """Выполняет запрос с валидацией через Pydantic"""
        url = f"{self.base_url}{endpoint}"

        json_data = request_model.model_dump(exclude_none=True) if request_model else None

        with allure.step(f"API {method} {endpoint}"):
            log.info(f"📤 {method} {url}")
            if json_data:
                log.debug(f"Request body: {json_data}")
                allure.attach(str(json_data), "Request Body", allure.attachment_type.JSON)

            response = self.session.request(
                method=method,
                url=url,
                json=json_data,
                timeout=self.timeout
            )

            log.info(f"📥 Response: {response.status_code}")

            assert response.status_code == expected_status, \
                f"Expected {expected_status}, got {response.status_code}. Response: {response.text}"

            if response_model:
                response_data = response.json()
                allure.attach(str(response_data), "Response Body", allure.attachment_type.JSON)
                return response_model.model_validate(response_data)

            return response

    # ========== API Methods ==========

    def signup(self, username: str, password: str) -> SignupResponse:
        """Регистрация нового пользователя"""
        request = SignupRequest(username=username, password=password)
        return self._request(
            method="POST",
            endpoint="/signup",
            request_model=request,
            response_model=SignupResponse,
            expected_status=200
        )

    def login(self, username: str, password: str) -> ErrorResponse:
        """Авторизация пользователя"""
        request = LoginRequest(username=username, password=password)
        return self._request(
            method="POST",
            endpoint="/login",
            request_model=request,
            response_model=ErrorResponse,
            expected_status=200
        )

    def get_products_by_category(self, category: str) -> ProductsResponse:
        """Получение товаров по категории"""
        request = ByCatRequest(cat=category)
        return self._request(
            method="POST",
            endpoint="/bycat",
            request_model=request,
            response_model=ProductsResponse,
            expected_status=200
        )

    def get_product_by_id(self, product_id: int) -> ProductResponse:
        """Получение товара по ID"""
        request = ViewProductRequest(id=product_id)
        return self._request(
            method="POST",
            endpoint="/view",
            request_model=request,
            response_model=ProductResponse,
            expected_status=200
        )


# Глобальный экземпляр клиента
api_client = ApiClient()