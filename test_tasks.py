from unittest.mock import MagicMock

from tasks import DataFetchingTask
from validators import ResponseValidator


class TestDataFetchingTask:
    def test_run(self, response):
        city_name = "MOSCOW"
        weather_api = MagicMock()
        weather_api.get_forecasting.return_value = response
        task = DataFetchingTask(city_name, weather_api, ResponseValidator)

        actual = task.run()

        assert actual.city == city_name
        assert len(actual.forecasts) == 5
