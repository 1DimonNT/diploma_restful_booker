"""Pydantic модели для Demoblaze API"""
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Union


# ========== Request Models ==========

class SignupRequest(BaseModel):
    """Модель запроса на регистрацию"""
    username: str = Field(..., min_length=3, max_length=50, description="Имя пользователя")
    password: str = Field(..., min_length=4, max_length=50, description="Пароль")


class LoginRequest(BaseModel):
    """Модель запроса на авторизацию"""
    username: str = Field(..., min_length=3, max_length=50, description="Имя пользователя")
    password: str = Field(..., min_length=4, max_length=50, description="Пароль")


class ByCatRequest(BaseModel):
    """Модель запроса для получения товаров по категории"""
    cat: str = Field(..., description="Категория товаров: phone, notebook, monitor")

    @field_validator("cat")
    @classmethod
    def validate_category(cls, v: str) -> str:
        allowed = ["phone", "notebook", "monitor"]
        if v not in allowed:
            raise ValueError(f"Category must be one of: {allowed}")
        return v


class ViewProductRequest(BaseModel):
    """Модель запроса для получения товара по ID"""
    id: int = Field(..., ge=1, description="ID товара")


# ========== Response Models ==========

class ProductResponse(BaseModel):
    """Модель товара"""
    id: int = Field(..., description="ID товара")
    title: str = Field(..., description="Название товара")
    price: int = Field(..., ge=0, description="Цена товара")
    desc: Optional[str] = Field(None, description="Описание товара")
    category: Optional[str] = Field(None, description="Категория товара")


class ProductsResponse(BaseModel):
    """Модель ответа со списком товаров"""
    Items: List[ProductResponse] = Field(default_factory=list, description="Список товаров")

    @property
    def count(self) -> int:
        return len(self.Items)


class ErrorResponse(BaseModel):
    """Модель ответа с ошибкой"""
    errorMessage: str = Field(..., description="Сообщение об ошибке")


class SignupResponse(BaseModel):
    """Модель ответа при регистрации (может быть строка или JSON)"""
    errorMessage: Optional[str] = None

    @classmethod
    def model_validate(cls, obj):
        """Кастомная валидация для пустой строки"""
        if obj == "":
            return cls(errorMessage=None)
        if isinstance(obj, dict):
            return cls(**obj)
        return cls(errorMessage=str(obj))

    @property
    def is_success(self) -> bool:
        return self.errorMessage is None