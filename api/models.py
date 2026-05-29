"""Pydantic модели для Demoblaze API (Pydantic v1)"""
from pydantic import BaseModel, Field, validator
from typing import List, Optional


# ========== Request Models ==========

class SignupRequest(BaseModel):
    """Модель запроса на регистрацию"""
    username: str
    password: str


class LoginRequest(BaseModel):
    """Модель запроса на авторизацию"""
    username: str
    password: str


class ByCatRequest(BaseModel):
    """Модель запроса для получения товаров по категории"""
    cat: str

    @validator("cat")
    def validate_category(cls, v: str) -> str:
        allowed = ["phone", "notebook", "monitor"]
        if v not in allowed:
            raise ValueError(f"Category must be one of: {allowed}")
        return v


class ViewProductRequest(BaseModel):
    """Модель запроса для получения товара по ID"""
    id: int


# ========== Response Models ==========

class ProductResponse(BaseModel):
    """Модель товара"""
    id: int
    title: str
    price: int
    desc: Optional[str] = None
    category: Optional[str] = None


class ProductsResponse(BaseModel):
    """Модель ответа со списком товаров"""
    Items: List[ProductResponse] = []

    @property
    def count(self) -> int:
        return len(self.Items)


class ErrorResponse(BaseModel):
    """Модель ответа с ошибкой"""
    errorMessage: str


class SignupResponse(BaseModel):
    """Модель ответа при регистрации (может быть строка или JSON)"""
    errorMessage: Optional[str] = None

    @classmethod
    def parse_obj(cls, obj):
        """Кастомная валидация для пустой строки (Pydantic v1)"""
        if obj == "":
            return cls(errorMessage=None)
        if isinstance(obj, dict):
            return cls(**obj)
        return cls(errorMessage=str(obj))

    @property
    def is_success(self) -> bool:
        return self.errorMessage is None