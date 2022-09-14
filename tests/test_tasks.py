import json
from pathlib import Path
from unittest.mock import MagicMock

from models import CityModel
from tasks import (
    DataAggregationTask,
    DataAnalyzingTask,
    DataCalculationTask,
    DataFetchingTask,
)
from tests.factories import CityModelFactory, DayModelFactory


class TestDataFetchingTask:
    def test_run(self, response):
        city_name = "MOSCOW"
        weather_api = MagicMock()
        weather_api.get_forecasting.return_value = response
        task = DataFetchingTask(city_name, weather_api, CityModel)

        actual = task.run()

        assert actual.city == city_name
        assert len(actual.days) == 5


class TestDataCalculationTask:
    def test_run(self):
        day = DayModelFactory.build()
        task = DataCalculationTask(day)
        task.run()

        assert day.avg_temp == 27
        assert day.clear_sum == 0


class TestDataAnalyzingTask:
    def test_run(self):
        cities = CityModelFactory.batch(10)
        path = Path("result.json")

        task = DataAnalyzingTask(cities, path)
        task.run()

        result = json.loads(path.read_text())
        assert len(result) == 10
        assert not result[0]["days"][0].get("hours")


class TestDataAggregationTask:
    def test_run(self):
        cities = CityModelFactory.batch(10)

        task = DataAggregationTask(cities)

        assert task.run() == cities[0]
