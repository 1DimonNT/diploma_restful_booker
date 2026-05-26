"""
API клиент для взаимодействия с Restful-booker сервисом.
Обеспечивает выполнение HTTP запросов с логированием и Allure вложениями.
"""

import json
import allure
import requests
from typing import Optional, Dict, Any
from requests import Response
from allure_commons.types import AttachmentType
from config import settings
from utils.logger import log, log_request, log_response
from utils.allure_helper import attach_request, attach_response


class ApiClient:
    """Клиент для работы с API Restful-booker"""

    def __init__(self):
        self.base_url = settings.api.full_base_url
        self.timeout = settings.api.timeout
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json", "Accept": "application/json"})
        self._token: Optional[str] = None

    @property
    def token(self) -> Optional[str]:
        """Получить текущий токен"""
        return self._token

    @token.setter
    def token(self, value: str):
        """Установить токен и добавить в заголовки"""
        self._token = value
        if value:
            self.session.headers.update({"Cookie": f"token={value}"})

    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict] = None,
        params: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        need_auth: bool = False,
    ) -> Response:
        """
        Выполнить HTTP запрос с логированием

        Args:
            method: HTTP метод (GET, POST, PUT, PATCH, DELETE)
            endpoint: endpoint (без base_url)
            data: тело запроса
            params: query параметры
            headers: дополнительные заголовки
            need_auth: требуется ли авторизация

        Returns:
            Response объект
        """
        url = f"{self.base_url}{endpoint}"

        # Логируем запрос
        log_request(method, url, headers, data)

        # Объединяем заголовки
        request_headers = self.session.headers.copy()
        if headers:
            request_headers.update(headers)

        # Выполняем запрос
        response = self.session.request(
            method=method, url=url, json=data, params=params, headers=request_headers, timeout=self.timeout
        )

        # Логируем ответ
        try:
            response_body = response.json()
        except:
            response_body = response.text

        log_response(response.status_code, response_body if isinstance(response_body, dict) else None)

        # Добавляем в Allure
        with allure.step(f"API Request: {method} {endpoint}"):
            attach_request(response, data)
            attach_response(response)

        return response

    def post(self, endpoint: str, data: Optional[Dict] = None, **kwargs) -> Response:
        """POST запрос"""
        return self._make_request("POST", endpoint, data=data, **kwargs)

    def get(self, endpoint: str, params: Optional[Dict] = None, **kwargs) -> Response:
        """GET запрос"""
        return self._make_request("GET", endpoint, params=params, **kwargs)

    def put(self, endpoint: str, data: Optional[Dict] = None, **kwargs) -> Response:
        """PUT запрос"""
        return self._make_request("PUT", endpoint, data=data, **kwargs)

    def patch(self, endpoint: str, data: Optional[Dict] = None, **kwargs) -> Response:
        """PATCH запрос"""
        return self._make_request("PATCH", endpoint, data=data, **kwargs)

    def delete(self, endpoint: str, **kwargs) -> Response:
        """DELETE запрос"""
        return self._make_request("DELETE", endpoint, **kwargs)

    def auth(self, username: str, password: str) -> str:
        """
        Аутентификация и получение токена

        Args:
            username: имя пользователя
            password: пароль

        Returns:
            токен авторизации
        """
        with allure.step(f"Аутентификация пользователя {username}"):
            response = self.post("/auth", data={"username": username, "password": password})
            assert response.status_code == 200, f"Auth failed with status {response.status_code}"

            token = response.json().get("token")
            assert token is not None, "Token not found in response"

            self.token = token
            log.info(f"✅ Authenticated successfully, token: {token[:10]}...")

            return token


# Создаем глобальный экземпляр клиента
api_client = ApiClient()
