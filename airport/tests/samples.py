import random
import string

from airport.models import Airport, Route, AirplaneType, Airplane, Crew


def sample_airport(**params):
    # Define the length of the random string you want
    string_length = 10  # Change this to your desired length

    # Generate a random string
    random_string = "".join(
        random.choice(string.ascii_letters + string.digits)
        for _ in range(string_length)
    )
    defaults = {
        "name": "Test" + str(random.randint(1, 10)),
        "closest_big_city": "Test" + random_string,
    }
    defaults.update(params)

    return Airport.objects.create(**defaults)


def sample_route(**params):
    first_airport = sample_airport()
    second_airport = sample_airport()
    data = {
        "source": first_airport,
        "destination": second_airport,
        "distance": 120,
    }
    data.update(params)
    return Route.objects.create(**data)


def sample_airplane_type(**params):
    data = {"name": "test_type"}
    data.update(params)
    return AirplaneType.objects.create(**data)


def sample_airplane(**params):
    airplane_type = sample_airplane_type()
    data = {
        "name": "test_airplane",
        "rows": 12,
        "seats_in_row": 2,
        "airplane_type": airplane_type,
    }
    data.update(params)
    return Airplane.objects.create(**data)


def sample_crew(**params):
    data = {"first_name": "test", "last_name": "test"}
    data.update(params)
    return Crew.objects.create(**data)
