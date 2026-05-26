"""
Pydantic модели для бронирования в Restful-booker API.
Включают модели для создания, обновления и получения бронирований.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime


class BookingDates(BaseModel):
    """Модель дат бронирования"""

    checkin: str = Field(..., description="Дата заезда (YYYY-MM-DD)")
    checkout: str = Field(..., description="Дата выезда (YYYY-MM-DD)")

    @field_validator("checkin", "checkout")
    @classmethod
    def validate_date_format(cls, v: str) -> str:
        """Валидация формата даты"""
        try:
            datetime.strptime(v, "%Y-%m-%d")
        except ValueError:
            raise ValueError(f"Invalid date format: {v}. Expected YYYY-MM-DD")
        return v

    model_config = {"json_schema_extra": {"examples": [{"checkin": "2024-12-01", "checkout": "2024-12-10"}]}}


class Booking(BaseModel):
    """Модель бронирования"""

    firstname: str = Field(..., description="Имя", min_length=1, max_length=50)
    lastname: str = Field(..., description="Фамилия", min_length=1, max_length=50)
    totalprice: int = Field(..., description="Общая стоимость", ge=0, le=1000000)
    depositpaid: bool = Field(..., description="Депозит оплачен")
    bookingdates: BookingDates = Field(..., description="Даты бронирования")
    additionalneeds: Optional[str] = Field(None, description="Дополнительные пожелания", max_length=200)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "firstname": "John",
                    "lastname": "Doe",
                    "totalprice": 150,
                    "depositpaid": True,
                    "bookingdates": {"checkin": "2024-12-01", "checkout": "2024-12-10"},
                    "additionalneeds": "Breakfast",
                }
            ]
        }
    }


class CreateBookingRequest(BaseModel):
    """Модель запроса на создание бронирования"""

    booking: Booking = Field(..., description="Данные бронирования")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "booking": {
                        "firstname": "John",
                        "lastname": "Doe",
                        "totalprice": 150,
                        "depositpaid": True,
                        "bookingdates": {"checkin": "2024-12-01", "checkout": "2024-12-10"},
                        "additionalneeds": "Breakfast",
                    }
                }
            ]
        }
    }


class CreateBookingResponse(BaseModel):
    """Модель ответа при создании бронирования"""

    bookingid: int = Field(..., description="ID созданного бронирования", ge=1)
    booking: Booking = Field(..., description="Данные созданного бронирования")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "bookingid": 1234,
                    "booking": {
                        "firstname": "John",
                        "lastname": "Doe",
                        "totalprice": 150,
                        "depositpaid": True,
                        "bookingdates": {"checkin": "2024-12-01", "checkout": "2024-12-10"},
                        "additionalneeds": "Breakfast",
                    },
                }
            ]
        }
    }


class UpdateBookingRequest(BaseModel):
    """Модель запроса на обновление бронирования"""

    firstname: Optional[str] = Field(None, description="Имя", min_length=1, max_length=50)
    lastname: Optional[str] = Field(None, description="Фамилия", min_length=1, max_length=50)
    totalprice: Optional[int] = Field(None, description="Общая стоимость", ge=0, le=1000000)
    depositpaid: Optional[bool] = Field(None, description="Депозит оплачен")
    bookingdates: Optional[BookingDates] = Field(None, description="Даты бронирования")
    additionalneeds: Optional[str] = Field(None, description="Дополнительные пожелания", max_length=200)


class GetBookingIdsResponse(BaseModel):
    """Модель ответа при получении списка ID бронирований"""

    bookingid: int = Field(..., description="ID бронирования")

    model_config = {"json_schema_extra": {"examples": [{"bookingid": 1}, {"bookingid": 2}, {"bookingid": 3}]}}
