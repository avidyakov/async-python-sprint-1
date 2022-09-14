import random

from pydantic_factories import ModelFactory, Use

from models import DayModel, HourModel


class HourModelFactory(ModelFactory):
    __model__ = HourModel

    hour = Use(random.randint, 9, 19)
    temp = 27.0


class DayModelFactory(ModelFactory):
    __model__ = DayModel

    hours = Use(HourModelFactory.batch, size=10)
