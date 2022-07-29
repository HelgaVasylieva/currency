from django import forms
from currency.models import Rate, Source


class RateForm(forms.ModelForm):
    class Meta:
        model = Rate
        fields = (
            'base_currency_type',
            'currency_type',
            'sale',
            'buy',
            'source'
        )


class SourceForm(forms.ModelForm):
    class Meta:
        model = Source
        fields = (
            'source_url',
            'name'
        )
