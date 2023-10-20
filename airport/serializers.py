from django.db import transaction
from rest_framework import serializers

from airport.models import (
	Airport,
	Route,
	AirplaneType,
	Airplane,
	Crew,
	Flight,
	Order,
	Ticket
)


class AirportSerializer(serializers.ModelSerializer):
	class Meta:
		model = Airport
		fields = "__all__"


class RouteSerializer(serializers.ModelSerializer):
	source = AirportSerializer(many=False)
	destination = AirportSerializer(many=False)
	
	class Meta:
		model = Route
		fields = "__all__"


class RouteCreateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Route
		fields = "__all__"


class AirplaneTypeSerializer(serializers.ModelSerializer):
	class Meta:
		model = AirplaneType
		fields = "__all__"


class AirplaneSerializer(serializers.ModelSerializer):
	class Meta:
		model = Airplane
		fields = ("id", "name", "rows", "seats_in_row", "airplane_type", "capacity")


class CrewSerializer(serializers.ModelSerializer):
	class Meta:
		model = Crew
		fields = "__all__"


class FlightSerializer(serializers.ModelSerializer):
	airplane = AirplaneSerializer(many=False)
	route = RouteSerializer(many=False)
	
	class Meta:
		model = Flight
		fields = ("id", "airplane", "route", "departure_time", "arrival_time")


class TicketSeatsSerializer(serializers.ModelSerializer):
	class Meta:
		model = Ticket
		fields = ("row", "seat")


class FlightDetailSerializer(serializers.ModelSerializer):
	airplane = AirplaneSerializer(many=False)
	route = RouteSerializer(many=False)
	taken_places = TicketSeatsSerializer(
		source="tickets", many=True, read_only=True
	)
	
	class Meta:
		model = Flight
		fields = ("id", "airplane", "route", "departure_time", "arrival_time", "taken_places")


class FlightCreateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Flight
		fields = ("id", "airplane", "route", "departure_time", "arrival_time")


class TicketSerializer(serializers.ModelSerializer):
	airplane = AirplaneSerializer(many=False, read_only=True)
	
	class Meta:
		model = Ticket
		fields = ("id", "row", "seat", "flight", "airplane")


class TicketListSerializer(TicketSerializer):
	flight = FlightSerializer(many=False, read_only=True)


class OrderSerializer(serializers.ModelSerializer):
	tickets = TicketSerializer(many=True, read_only=False, allow_null=False)
	
	class Meta:
		model = Order
		fields = ("id", "tickets", "created_at")
	
	def create(self, validated_data):
		with transaction.atomic():
			tickets_data = validated_data.pop("tickets")
			order = Order.objects.create(**validated_data)
			for ticket_data in tickets_data:
				Ticket.objects.create(order=order, **ticket_data)
			return order


class OrderListSerializer(OrderSerializer):
	tickets = TicketListSerializer(many=True, read_only=True)
