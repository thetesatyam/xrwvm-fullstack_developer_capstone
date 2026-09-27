import json
from pathlib import Path

from .models import CarMake, CarModel


def initiate():
    data_file = (
        Path(__file__).resolve().parents[1]
        / "database"
        / "data"
        / "car_records.json"
    )

    with open(data_file, "r", encoding="utf-8") as file:
        cars = json.load(file)["cars"]

    for car in cars:
        car_make, _ = CarMake.objects.get_or_create(
            name=car["make"],
            defaults={
                "description": f"{car['make']} cars"
            }
        )

        CarModel.objects.get_or_create(
            car_make=car_make,
            name=car["model"],
            year=car["year"],
            defaults={
                "type": car["bodyType"]
            }
        )

    print("Car Make and Car Model data populated successfully.")