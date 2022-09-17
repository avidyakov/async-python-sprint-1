from pydantic import BaseModel, Field, validator


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
        try:
            return sum(hour.temp for hour in self.hours) / len(self.hours)
        except ZeroDivisionError:
            return 0.0

    def get_clear_sum(self) -> int:
        return sum(hour.is_clear() for hour in self.hours)

    @validator("hours")
    def filter_hours(cls, hours: list[HourModel]) -> list[HourModel]:
        return [hour for hour in hours if 9 <= hour.hour <= 19]


class CityModel(BaseModel):
    city: str
    days: list[DayModel] = Field(alias="forecasts")
    score: float | None

    def get_score(self) -> float:
        try:
            # Складываю среднюю температуру за день
            # и количество часов за день с ясной погодой
            return sum(day.avg_temp + day.clear_sum for day in self.days)
        except TypeError:
            return 0.0
