from pydantic import BaseModel

from utils import YandexWeatherAPI


class DataFetchingTask:
    def __init__(
        self, city: str, ya_weather_api: YandexWeatherAPI, validator: type[BaseModel]
    ) -> None:
        self.city = city
        self.ya_weather_api = ya_weather_api
        self.validator = validator

    def run(self) -> BaseModel:
        response = self.ya_weather_api.get_forecasting(self.city)
        return self.validator(city=self.city, **response)


class DataCalculationTask:
    pass


class DataAggregationTask:
    pass


class DataAnalyzingTask:
    pass
