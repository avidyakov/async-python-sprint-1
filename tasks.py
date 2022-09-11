from pydantic import BaseModel

from utils import YandexWeatherAPI


class DataFetchingTask:
    def __init__(
        self, city: str, weather_api: YandexWeatherAPI, validator: BaseModel
    ) -> None:
        self.city = city
        self.weather_api = weather_api
        self.validator = validator

    def run(self) -> BaseModel:
        response = self.weather_api.get_forecasting(self.city)
        return self.validator(city=self.city, **response)


class DataCalculationTask:
    pass


class DataAggregationTask:
    pass


class DataAnalyzingTask:
    pass
