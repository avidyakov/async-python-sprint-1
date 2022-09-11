from datetime import date
from typing import Any

from pydantic import BaseModel


class HourValidator(BaseModel):
    hour: int
    temp: float
    condition: str


class ForecastValidator(BaseModel):
    date: date
    hours: list[HourValidator]

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)
        self.hours = [hour for hour in self.hours if 9 <= hour.hour <= 19]


class ResponseValidator(BaseModel):
    city: str
    forecasts: list[ForecastValidator]
