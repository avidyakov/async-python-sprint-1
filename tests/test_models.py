import pytest

from models import CityModel, DayModel, HourModel
from tests.factories import CityModelFactory, DayModelFactory


class TestResponseValidator:
    def test_validate_response(self, response):
        validator = CityModel(city="Moscow", **response)

        assert len(validator.days) == 5
        assert validator.days[0].hours[0].hour == 9
        assert validator.days[0].hours[-1].hour == 19
        assert len(validator.days[0].hours) == 11


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


class TestDayModel:
    @pytest.mark.parametrize(
        "hours, expected",
        (
            (
                [
                    {"hour": 9, "temp": 10.0, "condition": "clear"},
                    {"hour": 10, "temp": 20.0, "condition": "clear"},
                    {"hour": 11, "temp": 30.0, "condition": "clear"},
                ],
                20,
            ),
            ([], 0.0),
        ),
    )
    def test_get_avg_temp(self, hours, expected):
        validator = DayModel(
            date="2021-01-01",
            hours=hours,
        )

        assert validator.get_avg_temp() == expected

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


class TestCityModel:
    def test_get_score(self):
        day1 = DayModelFactory.build(avg_temp=10, clear_sum=5)
        day2 = DayModelFactory.build(avg_temp=17, clear_sum=3)
        city = CityModelFactory.build(forecasts=[day1, day2])

        assert city.get_score() == 35

    def test_get_score_with_none(self):
        city = CityModelFactory.build()

        assert city.get_score() == 0
