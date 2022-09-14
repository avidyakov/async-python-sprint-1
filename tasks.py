from pydantic import BaseModel

from models import DayModel
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


class DataAggregationTask:
    pass


class DataAnalyzingTask:
    pass
