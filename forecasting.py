from multiprocessing.pool import Pool, ThreadPool
from pathlib import Path

from models import CityModel
from tasks import (
    DataAggregationTask,
    DataAnalyzingTask,
    DataCalculationTask,
    DataFetchingTask,
)
from utils import CITIES, YandexWeatherAPI


def run_task(task):
    return task.run()


def forecast_weather(path: Path) -> None:
    """
    Анализ погодных условий по городам
    """
    fetching_tasks = [
        DataFetchingTask(city, YandexWeatherAPI(), CityModel)
        for city in CITIES
    ]
    with ThreadPool(processes=8) as pool:  # Пул потоков
        cities = pool.map(run_task, fetching_tasks)

    calculation_tasks = [DataCalculationTask(city) for city in cities]
    with Pool(processes=2) as pool:  # Пул процессов
        cities = pool.map(run_task, calculation_tasks)

    analyzing_task = DataAnalyzingTask(cities, path)
    analyzing_task.run()

    aggregation_task = DataAggregationTask(cities)
    aggregation_task.run()


if __name__ == "__main__":
    result_path = Path(__file__).parent / "result.json"
    forecast_weather(result_path)
