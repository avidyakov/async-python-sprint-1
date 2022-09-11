from datetime import date
from typing import Any

from pydantic import BaseModel


class HourModel(BaseModel):
    hour: int
    temp: float
    condition: str
    _clear_weather = {"clear", "partly-cloudy", "cloudy", "overcast"}

    def is_clear(self) -> bool:
        return self.condition in self._clear_weather


class DayModel(BaseModel):
    date: date
    hours: list[HourModel]

    def get_avg_temp(self) -> float:
        return sum(hour.temp for hour in self.hours) / len(self.hours)

    def get_clear_sum(self) -> int:
        return sum(hour.is_clear() for hour in self.hours)

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)
        self.hours = [hour for hour in self.hours if 9 <= hour.hour <= 19]


class CityModel(BaseModel):
    city: str
    forecasts: list[DayModel]
