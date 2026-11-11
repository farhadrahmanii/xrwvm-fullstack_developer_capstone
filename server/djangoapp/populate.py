from .models import CarMake, CarModel


def initiate():
    car_make_data = [
        {"name": "NISSAN", "description": "Great cars. Japanese technology"},
        {"name": "Mercedes", "description": "Great cars. German technology"},
        {"name": "Audi", "description": "Great cars. German technology"},
        {"name": "Kia", "description": "Great cars. Korean technology"},
        {"name": "Toyota", "description": "Great cars. Japanese technology"},
    ]

    makes = []
    for data in car_make_data:
        makes.append(CarMake.objects.create(
            name=data['name'], description=data['description']))

    car_model_data = [
        ("Pathfinder", "SUV", 2023, 0), ("Qashqai", "SUV", 2023, 0),
        ("XTRAIL", "SUV", 2023, 0), ("A-Class", "SUV", 2023, 1),
        ("C-Class", "SUV", 2023, 1), ("E-Class", "SUV", 2023, 1),
        ("A4", "SUV", 2023, 2), ("A5", "SUV", 2023, 2),
        ("A6", "SUV", 2023, 2), ("Sorrento", "SUV", 2023, 3),
        ("Carnival", "SUV", 2023, 3), ("Cerato", "SEDAN", 2023, 3),
        ("Corolla", "SEDAN", 2023, 4), ("Camry", "SEDAN", 2023, 4),
        ("Kluger", "SUV", 2023, 4),
    ]

    for name, car_type, year, make_index in car_model_data:
        CarModel.objects.create(
            name=name, type=car_type, year=year,
            car_make=makes[make_index])
