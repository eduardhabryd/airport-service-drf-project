from django.contrib.auth import get_user_model
from django.db import models


class Airport(models.Model):
    name = models.CharField(max_length=100)
    closest_big_city = models.CharField(max_length=100)

    def __str__(self):
        return f"AIRPORT: {self.name}. CITY: {self.closest_big_city}"


class Route(models.Model):
    source = models.ForeignKey(
        Airport, related_name="source_routes", on_delete=models.CASCADE
    )
    destination = models.ForeignKey(
        Airport, related_name="destination_routes", on_delete=models.CASCADE
    )
    distance = models.IntegerField()

    def __str__(self):
        return (
            f"ROUTE: {self.source.closest_big_city} - "
            f"{self.destination.closest_big_city}. "
            f"DISTANCE: {self.distance}"
        )


class AirplaneType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"TYPE: {self.name}"


class Airplane(models.Model):
    name = models.CharField(max_length=100)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()
    airplane_type = models.ForeignKey(
        AirplaneType, related_name="airplanes", on_delete=models.CASCADE
    )

    @property
    def capacity(self):
        return self.rows * self.seats_in_row

    def __str__(self):
        return f"AIRPLANE: {self.name}"


class Crew(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return f"CREW MEMBER: {self.first_name} {self.last_name}"


class Flight(models.Model):
    route = models.ForeignKey(
        Route, related_name="flights", on_delete=models.CASCADE
    )
    airplane = models.ForeignKey(
        Airplane, related_name="flights", on_delete=models.CASCADE
    )
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    crew = models.ManyToManyField(
        Crew, related_name="flights"
    )

    def __str__(self):
        return (
            f"FLIGHT: {self.departure_time} - "
            f"{self.arrival_time}. "
            f"ROUTE: {self.route}"
        )


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        get_user_model(), related_name="orders", on_delete=models.CASCADE
    )


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    flight = models.ForeignKey(
        Flight, related_name="tickets", on_delete=models.CASCADE
    )
    order = models.ForeignKey(
        Order, related_name="tickets", on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ("flight", "row", "seat")
        ordering = ["row", "seat"]
