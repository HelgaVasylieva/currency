import django_filters
from currency.models import Rate


class RateFilter(django_filters.FilterSet):
    class Meta:
        model = Rate
        fields = {
            'buy': ('gte', 'lte'),
            'sale': ('gte', 'lte'),
            'source': ('exact', ),
            'base_currency_type': ('exact', ),
            'currency_type': ('exact', ),
        }
