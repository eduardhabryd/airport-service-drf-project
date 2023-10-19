from datetime import datetime

from django.db.models import F, Count
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

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
from airport.permissions import IsAdminOrIfAuthenticatedReadOnly

from airport.serializers import (
	AirportSerializer,
	RouteSerializer,
	AirplaneTypeSerializer,
	AirplaneSerializer,
	CrewSerializer,
	FlightSerializer,
	OrderSerializer,
	TicketSerializer
)


class AirportViewSet(
	mixins.ListModelMixin,
	GenericViewSet,
):
	queryset = Airport.objects.all()
	serializer_class = AirportSerializer
	

class RouteViewSet(
	mixins.ListModelMixin,
	GenericViewSet,
):
	queryset = Route.objects.all()
	serializer_class = RouteSerializer
	

class AirplaneTypeViewSet(
	mixins.ListModelMixin,
	GenericViewSet,
):
	queryset = AirplaneType.objects.all()
	serializer_class = AirplaneTypeSerializer
	

class AirplaneViewSet(
	mixins.ListModelMixin,
	GenericViewSet,
):
	queryset = Airplane.objects.all()
	serializer_class = AirplaneSerializer


class CrewViewSet(
	mixins.ListModelMixin,
	GenericViewSet,
):
	queryset = Crew.objects.all()
	serializer_class = CrewSerializer


class FlightViewSet(
	mixins.ListModelMixin,
	GenericViewSet,
):
	queryset = Flight.objects.all()
	serializer_class = FlightSerializer
	
	
class OrderViewSet(
	mixins.ListModelMixin,
	GenericViewSet,
):
	queryset = Order.objects.all()
	serializer_class = OrderSerializer
	

class TicketViewSet(
	mixins.ListModelMixin,
	GenericViewSet,
):
	queryset = Ticket.objects.all()
	serializer_class = TicketSerializer
