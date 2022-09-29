from django import forms
from currency.models import Rate, Source, ContactUs


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

        widgets = {
            'base_currency_type': forms.TextInput(attrs={'placeholder': 'Base currency'}),
            'currency_type': forms.TextInput(attrs={'placeholder': 'Currency'}),
            'sale': forms.TextInput(attrs={'placeholder': 'Sale'}),
            'buy': forms.TextInput(attrs={'placeholder': 'Buy'}),
            'source': forms.TextInput(attrs={'placeholder': 'Source'})
        }


class SourceForm(forms.ModelForm):
    class Meta:
        model = Source
        fields = (
            'source_url',
            'name',
            'logo'
        )


class ContactUsForm(forms.ModelForm):

    class Meta:
        model = ContactUs
        fields = (
            'email_from',
            'email_to',
            'subject',
            'message'
        )

    email_from = forms.EmailField()
    email_to = forms.EmailField()
    subject = forms.CharField()
    message = forms.CharField(widget=forms.Textarea())
