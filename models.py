from typing import Any

from pydantic import BaseModel, Field


class HourModel(BaseModel):
    hour: int
    temp: float
    condition: str
    _clear_weather = {"clear", "partly-cloudy", "cloudy", "overcast"}

    def is_clear(self) -> bool:
        return self.condition in self._clear_weather


class DayModel(BaseModel):
    date: str
    hours: list[HourModel] = Field(exclude=True)
    avg_temp: float | None
    clear_sum: int | None

    def get_avg_temp(self) -> float:
        return sum(hour.temp for hour in self.hours) / len(self.hours)

    def get_clear_sum(self) -> int:
        return sum(hour.is_clear() for hour in self.hours)

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)
        self.hours = [hour for hour in self.hours if 9 <= hour.hour <= 19]


class CityModel(BaseModel):
    city: str
    days: list[DayModel] = Field(alias="forecasts")

    def get_score(self) -> float:
        try:
            return sum(day.avg_temp + day.clear_sum for day in self.days)
        except TypeError:
            return 0.0
