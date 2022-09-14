import random

from pydantic_factories import ModelFactory, Use

from models import CityModel, DayModel, HourModel


class HourModelFactory(ModelFactory):
    __model__ = HourModel

    hour = Use(random.randint, 9, 19)
    temp = 27.0


class DayModelFactory(ModelFactory):
    __model__ = DayModel

    hours = Use(HourModelFactory.batch, size=10)


class CityModelFactory(ModelFactory):
    __model__ = CityModel

    forecasts = Use(DayModelFactory.batch, size=5)
