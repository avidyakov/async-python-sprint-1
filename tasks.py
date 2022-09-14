import json
from pathlib import Path

from pydantic import BaseModel

from models import CityModel, DayModel
from utils import YandexWeatherAPI


class DataFetchingTask:
    def __init__(
        self,
        city: str,
        ya_weather_api: YandexWeatherAPI,
        validator: type[BaseModel],
    ) -> None:
        self.city = city
        self.ya_weather_api = ya_weather_api
        self.validator = validator

    def run(self) -> BaseModel:
        response = self.ya_weather_api.get_forecasting(self.city)
        return self.validator(city=self.city, **response)


class DataCalculationTask:
    def __init__(self, day: DayModel) -> None:
        self.day = day

    def run(self) -> None:
        self.day.avg_temp = self.day.get_avg_temp()
        self.day.clear_sum = self.day.get_clear_sum()


class DataAnalyzingTask:
    def __init__(self, cities: list[CityModel], path: Path) -> None:
        self.cities = cities
        self.path = path

    def run(self) -> None:
        result = [city.dict() for city in self.cities]
        self.path.write_text(json.dumps(result, indent=4))


class DataAggregationTask:
    pass
