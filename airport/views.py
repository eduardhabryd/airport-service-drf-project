from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from collections import OrderedDict
from . import urls
from rest_framework import permissions, views
from rest_framework.response import Response
from rest_framework.reverse import NoReverseMatch, reverse

from airport.models import (
    Airport,
    Route,
    AirplaneType,
    Airplane,
    Crew,
    Flight,
    Order,
)
from airport.permissions import (
    IsAdminOrIfAuthenticatedReadOnly,
    AnonimUserPermissions,
)

from airport.serializers import (
    AirportSerializer,
    RouteListSerializer,
    RouteDetailSerializer,
    AirplaneTypeSerializer,
    AirplaneSerializer,
    CrewSerializer,
    FlightSerializer,
    OrderSerializer,
    OrderListSerializer,
    RouteCreateSerializer,
    FlightCreateSerializer,
    FlightDetailSerializer,
)

from airport.pagination import OrderPagination


class AirportViewSet(ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    pagination_class = OrderPagination

    def get_permissions(self):
        if self.request.user.is_anonymous:
            self.permission_classes = [
                AnonimUserPermissions,
            ]
        else:
            self.permission_classes = [
                IsAdminOrIfAuthenticatedReadOnly,
            ]

        return super(AirportViewSet, self).get_permissions()


class RouteViewSet(ModelViewSet):
    queryset = Route.objects.select_related("source", "destination")
    serializer_class = RouteListSerializer
    pagination_class = OrderPagination

    def get_permissions(self):
        if self.request.user.is_anonymous:
            self.permission_classes = [
                AnonimUserPermissions,
            ]
        else:
            self.permission_classes = [
                IsAdminOrIfAuthenticatedReadOnly,
            ]

        return super(RouteViewSet, self).get_permissions()

    def get_serializer_class(self):
        if self.action == "create":
            return RouteCreateSerializer

        if self.action == "retrieve":
            return RouteDetailSerializer

        return self.serializer_class


class AirplaneTypeViewSet(ModelViewSet):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer
    pagination_class = OrderPagination
    permission_classes = (IsAdminUser,)


class AirplaneViewSet(ModelViewSet):
    queryset = Airplane.objects.all()
    serializer_class = AirplaneSerializer
    pagination_class = OrderPagination
    permission_classes = (IsAdminUser,)


class CrewViewSet(ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer
    pagination_class = OrderPagination
    permission_classes = (IsAdminUser,)


class FlightViewSet(ModelViewSet):
    queryset = Flight.objects.select_related(
        "route__source", "route__destination", "airplane"
    ).prefetch_related("crew")
    pagination_class = OrderPagination
    serializer_class = FlightSerializer

    def get_permissions(self):
        if self.request.user.is_anonymous:
            self.permission_classes = [
                AnonimUserPermissions,
            ]
        else:
            self.permission_classes = [
                IsAdminOrIfAuthenticatedReadOnly,
            ]

        return super(FlightViewSet, self).get_permissions()

    def get_serializer_class(self):
        if self.action == "create":
            return FlightCreateSerializer
        if self.action == "update":
            return FlightCreateSerializer
        if self.action == "retrieve":
            return FlightDetailSerializer

        return self.serializer_class

    def get_queryset(self):
        source = self.request.query_params.get("source")
        destination = self.request.query_params.get("destination")

        queryset = self.queryset

        if source:
            queryset = queryset.filter(
                route__source__closest_big_city__icontains=source
            )

        if destination:
            queryset = queryset.filter(
                route__destination__closest_big_city__icontains=destination
            )

        return queryset


class OrderViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet,
):
    queryset = Order.objects.prefetch_related(
        "tickets__flight",
        "tickets__flight__route__source",
        "tickets__flight__route__destination",
    )
    serializer_class = OrderSerializer
    pagination_class = OrderPagination
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = self.queryset
        if not self.request.user.is_staff:
            return queryset.filter(user=self.request.user)

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return OrderListSerializer

        return OrderSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class APIRootView(views.APIView):
    _ignore_model_permissions = True
    exclude_from_schema = True

    def get(self, request, *args, **kwargs):
        ret = OrderedDict()
        namespace = request.resolver_match.namespace
        for key, url_name in self.get_api_root_dict(request).items():
            if namespace:
                url_name = namespace + ":" + url_name
            try:
                ret[key] = reverse(
                    url_name,
                    args=args,
                    kwargs=kwargs,
                    request=request,
                    format=kwargs.get("format", None),
                )
            except NoReverseMatch:
                continue

        return Response(ret)

    def get_api_root_dict(self, request):
        api_root_dict = OrderedDict()
        list_name = urls.router.routes[0].name
        for prefix, viewset, basename in urls.router.registry:
            if self.check_permissions_with_viewset(request, viewset):
                api_root_dict[prefix] = list_name.format(basename=basename)
        return api_root_dict

    def check_permissions_with_viewset(self, request, viewset):
        for permission in viewset.permission_classes:
            if isinstance(permission, permissions.AllowAny):
                return True
            elif not permission().has_permission(request, viewset):
                return False
        return True
