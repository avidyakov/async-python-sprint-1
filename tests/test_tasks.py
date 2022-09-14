from unittest.mock import MagicMock

from models import CityModel
from tasks import DataCalculationTask, DataFetchingTask
from tests.factories import DayModelFactory


class TestDataFetchingTask:
    def test_run(self, response):
        city_name = "MOSCOW"
        weather_api = MagicMock()
        weather_api.get_forecasting.return_value = response
        task = DataFetchingTask(city_name, weather_api, CityModel)

        actual = task.run()

        assert actual.city == city_name
        assert len(actual.forecasts) == 5


class TestDataCalculationTask:
    def test_run(self):
        day = DayModelFactory.build()
        task = DataCalculationTask(day)
        task.run()

        assert day.avg_temp == 27
        assert day.clear_sum == 0
