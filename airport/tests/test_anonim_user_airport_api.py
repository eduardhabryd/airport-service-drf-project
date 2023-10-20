import datetime

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from .samples import *
from .airport_urls import *


ALLOWED_URLS = [AIRPORTS_URL, ROUTES_URL, FLIGHTS_URL]

FORBIDDEN_URLS = [ORDERS_URL, AIRPLANE_TYPES_URL, AIRPLANE_URL, CREW_URL]


class UnauthenticatedAirportApiTestsForbiddenUrlsGet(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        for url in FORBIDDEN_URLS:
            print(url)
            res = self.client.get(url)
            self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class UnauthenticatedAirportApiTestsAllowedUrlsGet(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_allowed(self):
        for url in ALLOWED_URLS:
            res = self.client.get(url)
            self.assertEqual(res.status_code, status.HTTP_200_OK)


class UnauthenticatedAirportApiTestsAllowedUrlsPostForbidden(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_post_airports(self):
        url = AIRPORTS_URL
        data = {"name": "Test", "closest_big_city": "Test"}
        print(url)
        res = self.client.post(url, data)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_routes(self):
        first_airport = sample_airport()
        second_airport = sample_airport()
        url = ROUTES_URL
        data = {
            "source": first_airport.pk,
            "destination": second_airport.pk,
            "distance": 120,
        }
        print(url)
        res = self.client.post(url, data)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_flights(self):
        route = sample_route()
        airplane = sample_airplane()
        crew = sample_crew()
        url = FLIGHTS_URL
        data = {
            "route": route.pk,
            "airplane": airplane.pk,
            "crew": [crew.pk],
            "departure_time": datetime.datetime.now(),
            "arrival_time": datetime.datetime.now()
            + datetime.timedelta(days=1),
        }
        print(url)
        res = self.client.post(url, data)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
