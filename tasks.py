import json
from pathlib import Path

from loguru import logger

from models import CityModel
from utils import YandexWeatherAPI


class DataFetchingTask:
    def __init__(
        self,
        city: str,
        ya_weather_api: YandexWeatherAPI,
        model: type[CityModel],
    ) -> None:
        self.city = city
        self.ya_weather_api = ya_weather_api
        self.model = model

    def run(self) -> CityModel:
        response = self.ya_weather_api.get_forecasting(self.city)
        model = self.model(city=self.city, **response)
        logger.info(f"Погода в городе {self.city} получена")
        return model


class DataCalculationTask:
    def __init__(self, city: CityModel) -> None:
        self.city = city

    def run(self) -> CityModel:
        for day in self.city.days:
            avg_temp = day.get_avg_temp()
            day.avg_temp = avg_temp
            logger.info(
                f"Средняя температура в городе {self.city.city} "
                f"на {day.date} составляет {avg_temp}"
            )

            clear_sum = day.get_clear_sum()
            day.clear_sum = clear_sum
            logger.info(
                f"Количество часов без осадков в городе {self.city.city} "
                f"на {day.date} составляет {clear_sum}"
            )

        return self.city


class DataAnalyzingTask:
    def __init__(self, cities: list[CityModel], path: Path) -> None:
        self.cities = cities
        self.path = path

    def run(self) -> None:
        result = [city.dict() for city in self.cities]
        self.path.write_text(json.dumps(result, indent=4))
        logger.info(f"Результат сохранен в {self.path}")


class DataAggregationTask:
    def __init__(self, cities: list[CityModel]) -> None:
        self.cities = cities

    def run(self) -> CityModel:
        best_city = max(self.cities, key=lambda city: city.get_score())
        logger.info(f"Лучший город: {best_city.city}")
        return best_city
