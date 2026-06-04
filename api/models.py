"""Pydantic модели для Demoblaze API (Pydantic v1)"""

from pydantic import BaseModel, Field, validator

# ========== Request Models ==========


class SignupRequest(BaseModel):
    """Модель запроса на регистрацию"""

    username: str = Field(..., description="Имя пользователя")
    password: str = Field(..., description="Пароль")


class LoginRequest(BaseModel):
    """Модель запроса на авторизацию"""

    username: str = Field(..., description="Имя пользователя")
    password: str = Field(..., description="Пароль")


class ByCatRequest(BaseModel):
    """Модель запроса для получения товаров по категории"""

    cat: str = Field(..., description="Категория товаров: phone, notebook, monitor")

    @validator("cat", check_fields=False)
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
    desc: str | None = Field(None, description="Описание товара")
    category: str | None = Field(None, description="Категория товара")


class ProductsResponse(BaseModel):
    """Модель ответа со списком товаров"""

    Items: list[ProductResponse] = Field(default_factory=list, description="Список товаров")

    @property
    def count(self) -> int:
        return len(self.Items)


class ErrorResponse(BaseModel):
    """Модель ответа с ошибкой"""

    errorMessage: str = Field(..., description="Сообщение об ошибке")


class SignupResponse(BaseModel):
    """Модель ответа при регистрации (может быть строка или JSON)"""

    errorMessage: str | None = Field(None, description="Сообщение об ошибке")

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
