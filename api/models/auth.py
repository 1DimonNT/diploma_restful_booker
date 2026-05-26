"""
Pydantic модели для авторизации в Restful-booker API.
Используются для валидации запросов и ответов.
"""

from pydantic import BaseModel, Field
from typing import Optional


class AuthRequest(BaseModel):
    """Модель запроса на авторизацию"""

    username: str = Field(..., description="Имя пользователя", min_length=1, max_length=50)
    password: str = Field(..., description="Пароль", min_length=1, max_length=50)

    model_config = {"json_schema_extra": {"examples": [{"username": "admin", "password": "password123"}]}}


class AuthResponse(BaseModel):
    """Модель ответа при авторизации"""

    token: str = Field(..., description="Токен авторизации для последующих запросов")

    model_config = {"json_schema_extra": {"examples": [{"token": "abc123def456ghi789"}]}}


class AuthErrorResponse(BaseModel):
    """Модель ответа при ошибке авторизации"""

    reason: Optional[str] = Field(None, description="Причина ошибки")

    model_config = {"json_schema_extra": {"examples": [{"reason": "Bad credentials"}]}}
