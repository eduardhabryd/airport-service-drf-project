from django.urls import reverse

AIRPORTS_URL = reverse("airport:airport-list")
ROUTES_URL = reverse("airport:route-list")
AIRPLANE_TYPES_URL = reverse("airport:airplanetype-list")
AIRPLANE_URL = reverse("airport:airplane-list")
CREW_URL = reverse("airport:crew-list")
FLIGHTS_URL = reverse("airport:flight-list")
ORDERS_URL = reverse("airport:order-list")
