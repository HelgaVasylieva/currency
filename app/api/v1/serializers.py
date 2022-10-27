from rest_framework.serializers import ModelSerializer

from currency.models import Rate, Source, ContactUs


class RateSerializer(ModelSerializer):
    class Meta:
        model = Rate
        fields = (
            'id',
            'buy',
            'sale',
            'currency_type',
            'base_currency_type',
            'created',
            'source',
        )


class SourceSerializer(ModelSerializer):
    class Meta:
        model = Source
        fields = (
            'name',
            'source_url',
        )


class ContactUsSerializer(ModelSerializer):
    class Meta:
        model = ContactUs
        fields = (
            'email_from',
            'email_to',
            'subject',
            'message'
        )
