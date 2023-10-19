from django.contrib.auth import get_user_model
from django.db import models


class Airport(models.Model):
	name = models.CharField(max_length=100)
	closest_big_city = models.CharField(max_length=100)


class Route(models.Model):
	source = models.ForeignKey(Airport, related_name="source_routes", on_delete=models.CASCADE)
	destination = models.ForeignKey(Airport, related_name="destination_routes", on_delete=models.CASCADE)
	distance = models.IntegerField()


class AirplaneType(models.Model):
	name = models.CharField(max_length=100)


class Airplane(models.Model):
	name = models.CharField(max_length=100)
	rows = models.IntegerField()
	seats_in_row = models.IntegerField()
	airplane_type = models.ForeignKey(AirplaneType, related_name="airplanes", on_delete=models.CASCADE)


class Crew(models.Model):
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)


class Flight(models.Model):
	route = models.ForeignKey(Route, related_name="flights", on_delete=models.CASCADE)
	airplane = models.ForeignKey(Airplane, related_name="flights", on_delete=models.CASCADE)
	departure_time = models.DateTimeField()
	arrival_time = models.DateTimeField()


class Order(models.Model):
	created_at = models.DateTimeField()
	user = models.ForeignKey(get_user_model(), related_name="orders", on_delete=models.CASCADE)


class Ticket(models.Model):
	row = models.IntegerField()
	seat = models.IntegerField()
	flight = models.ForeignKey(Flight, related_name="tickets", on_delete=models.CASCADE)
	order = models.ForeignKey(Order, related_name="tickets", on_delete=models.CASCADE)
