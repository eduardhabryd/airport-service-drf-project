import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from .samples import *
from .airport_urls import *


ALLOWED_URLS = [
	AIRPORTS_URL,
	ROUTES_URL,
	FLIGHTS_URL,
	ORDERS_URL,
]

FORBIDDEN_URLS = [
	AIRPLANE_TYPES_URL,
	AIRPLANE_URL,
	CREW_URL
]



class AuthAirportApiTestsForbiddenUrlsGet(TestCase):
	def setUp(self):
		self.client = APIClient()
		self.user = get_user_model().objects.create_user(
			"test@test.com",
			"testpass",
		)
		self.client.force_authenticate(self.user)
	
	def test_auth_required(self):
		for url in FORBIDDEN_URLS:
			print(url)
			res = self.client.get(url)
			self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AuthAirportApiTestsAllowedUrlsGet(TestCase):
	def setUp(self):
		self.client = APIClient()
		self.user = get_user_model().objects.create_user(
			"test@test.com",
			"testpass",
		)
		self.client.force_authenticate(self.user)
	
	def test_allowed(self):
		for url in ALLOWED_URLS:
			print(url)
			res = self.client.get(url)
			self.assertEqual(res.status_code, status.HTTP_200_OK)