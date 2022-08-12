from django.contrib import admin
from currency.models import Rate, Source, ContactUs

from rangefilter.filters import DateTimeRangeFilter
from import_export.admin import ImportExportModelAdmin


class RateAdmin(ImportExportModelAdmin):
    list_display = (
        'id',
        'base_currency_type',
        'currency_type',
        'sale',
        'buy',
    )
    readonly_fields = (
        'sale',
        'buy',
    )
    search_fields = (
        'base_currency_type',
        'currency_type',
        'sale',
        'buy',
    )
    list_filter = (
        'base_currency_type',
        ('created', DateTimeRangeFilter),
    )

    def has_delete_permission(self, request, obj=None):
        return False


class SourceAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'source_url',
        'name',
    )


class ContactUsAdmin(admin.ModelAdmin):
    list_display = (
        'email_from',
        'email_to',
        'subject',
        'message',
    )
    readonly_fields = (
        'email_from',
        'email_to',
        'subject',
        'message',
    )

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False


admin.site.register(Rate, RateAdmin)
admin.site.register(Source, SourceAdmin)
admin.site.register(ContactUs, ContactUsAdmin)
