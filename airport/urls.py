from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from airport.views import (
	AirportViewSet,
	RouteViewSet,
	AirplaneTypeViewSet,
	AirplaneViewSet,
	CrewViewSet,
	FlightViewSet,
	OrderViewSet,
	TicketViewSet
)

router = routers.DefaultRouter()
router.register("airports", AirportViewSet)
router.register("routes", RouteViewSet)
router.register("airplane-types", AirplaneTypeViewSet)
router.register("airplanes", AirplaneViewSet)
router.register("crew", CrewViewSet)
router.register("flights", FlightViewSet)
router.register("orders", OrderViewSet)
router.register("tickets", TicketViewSet)

urlpatterns = [path("api/", include(router.urls))]

app_name = "airport"
