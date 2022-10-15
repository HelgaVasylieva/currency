from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from django_filters import rest_framework as filters
from rest_framework import filters as rest_framework_filters

from currency.tasks import send_contact_us_email
from currency.models import Rate, Source, ContactUs
from api.serializers import RateSerializer, SourceSerializer, ContactUsSerializer
from api.pagination import RatePagination
from api.filters import RateFilter, SourceFilter, ContactUsFilter
from api.throttles import AnonCurrencyModelThrottle


class RatesView(generics.ListCreateAPIView):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer
    pagination_class = RatePagination
    filterset_class = RateFilter
    filter_backends = (
        filters.DjangoFilterBackend,
        rest_framework_filters.OrderingFilter,
    )
    ordering_fields = ['id', 'buy', 'sale']
    throttle_classes = [AnonCurrencyModelThrottle]


class RateDetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer


class SourceViewSet(generics.ListAPIView):
    queryset = Source.objects.all()
    serializer_class = SourceSerializer
    filterset_class = SourceFilter
    filter_backends = (
        filters.DjangoFilterBackend,
        rest_framework_filters.OrderingFilter,
    )
    ordering_fields = ['id', 'name']


class ContactUsViewSet(ModelViewSet):
    queryset = ContactUs.objects.all()
    serializer_class = ContactUsSerializer
    filterset_class = ContactUsFilter
    filter_backends = (
        filters.DjangoFilterBackend,
        rest_framework_filters.OrderingFilter,
        rest_framework_filters.SearchFilter,
    )
    search_fields = ['subject', 'message']
    ordering_fields = ['id', 'subject', 'message']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        email_from = serializer.validated_data['email_from']
        subject = serializer.validated_data['subject']
        send_contact_us_email.delay(subject, email_from)

        return Response(serializer.data)
