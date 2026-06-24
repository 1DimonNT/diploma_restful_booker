"""
API клиент для работы с товарами
"""

import allure
import requests

from config import settings
from utils.logger import log_request, log_response


class ProductsClient:
    def __init__(self):
        self.base_url = settings.api_base_url
        self.timeout = settings.api_timeout
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})

    def _request(self, method: str, endpoint: str, json_data: dict | None = None):
        url = f"{self.base_url}{endpoint}"

        with allure.step(f"API {method} {endpoint}"):
            log_request(method, url, body=json_data)
            response = self.session.request(method=method, url=url, json=json_data, timeout=self.timeout)
            log_response(response.status_code, body=response.json() if response.text else None)
            return response

    def get_by_category(self, category: str):
        return self._request("POST", "/bycat", {"cat": category})

    def get_by_id(self, product_id: int):
        return self._request("POST", "/view", {"id": product_id})


products_client = ProductsClient()
