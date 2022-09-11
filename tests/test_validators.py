import pytest

from models import CityModel, DayModel, HourModel


class TestResponseValidator:
    def test_validate_response(self, response):
        validator = CityModel(city="Moscow", **response)

        assert len(validator.forecasts) == 5
        assert validator.forecasts[0].hours[0].hour == 9
        assert validator.forecasts[0].hours[-1].hour == 19
        assert len(validator.forecasts[0].hours) == 11


class TestHourValidator:
    @pytest.mark.parametrize(
        "condition, expected",
        [
            ("clear", True),
            ("drizzle", False),
        ],
    )
    def test_is_with_precipitation(self, condition, expected):
        validator = HourModel(hour=12, temp=10.0, condition=condition)
        assert validator.is_clear() is expected


class TestForecastValidator:
    def test_get_avg_temp(self):
        validator = DayModel(
            date="2021-01-01",
            hours=[
                {"hour": 9, "temp": 10.0, "condition": "clear"},
                {"hour": 10, "temp": 20.0, "condition": "clear"},
                {"hour": 11, "temp": 30.0, "condition": "clear"},
            ],
        )

        assert validator.get_avg_temp() == 20

    def test_get_clear_sum(self):
        validator = DayModel(
            date="2021-01-01",
            hours=[
                {"hour": 9, "temp": 10.0, "condition": "clear"},
                {"hour": 10, "temp": 20.0, "condition": "cloudy"},
                {"hour": 11, "temp": 30.0, "condition": "drizzle"},
            ],
        )

        assert validator.get_clear_sum() == 2
