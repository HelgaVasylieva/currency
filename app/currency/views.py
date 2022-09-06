import io
import csv

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.http import HttpResponse
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.conf import settings
from django.views import generic

from currency.models import Rate, ContactUs, Source
from currency.forms import RateForm, SourceForm, ContactUsForm


class IndexView(generic.TemplateView):
    template_name = 'index.html'


class RateListView(generic.ListView):
    queryset = Rate.objects.all().select_related('source')
    template_name = 'rate_list.html'


class RateCreateView(generic.CreateView):
    queryset = Rate.objects.all()
    template_name = 'rate_create.html'
    form_class = RateForm
    success_url = reverse_lazy('currency:rate_list')


class RateUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    queryset = Rate.objects.all()
    template_name = 'rate_update.html'
    form_class = RateForm
    success_url = reverse_lazy('currency:rate_list')

    def test_func(self):
        return self.request.user.is_superuser


class RateDetailsView(LoginRequiredMixin, generic.DeleteView):
    queryset = Rate.objects.all()
    template_name = 'rate_details.html'


class RateDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    queryset = Rate.objects.all()
    template_name = 'rate_delete.html'
    success_url = reverse_lazy('currency:rate_list')

    def test_func(self):
        return self.request.user.is_superuser


class DownloadRateView(generic.View):
    def get(self, request):
        csvfile = io.StringIO()
        spamwriter = csv.writer(csvfile)
        headers = ['id', 'buy', 'sale']
        spamwriter.writerow(headers)
        for rate in Rate.objects.all():
            row = [
                rate.id,
                rate.buy,
                rate.sale,
            ]
            spamwriter.writerow(row)

        csvfile.seek(0)
        return HttpResponse(csvfile.read(), content_type='text/csv')


class SourceListView(generic.ListView):
    queryset = Source.objects.all()
    template_name = 'source_list.html'


class SourceCreateView(generic.CreateView):
    queryset = Source.objects.all()
    template_name = 'source_create.html'
    form_class = SourceForm
    success_url = reverse_lazy('currency:source_list')


class SourceUpdateView(generic.UpdateView):
    queryset = Source.objects.all()
    template_name = 'source_update.html'
    form_class = SourceForm
    success_url = reverse_lazy('currency:source_list')


class SourceDetailsView(generic.DeleteView):
    queryset = Source.objects.all()
    template_name = 'source_details.html'


class SourceDeleteView(generic.DeleteView):
    queryset = Source.objects.all()
    template_name = 'source_delete.html'
    success_url = reverse_lazy('currency:source_list')


class ContactListView(generic.ListView):
    queryset = ContactUs.objects.all()
    template_name = 'contact_list.html'


class ContactUsCreateView(generic.CreateView):
    queryset = ContactUs.objects.all()
    template_name = 'contactus_create.html'
    form_class = ContactUsForm
    success_url = reverse_lazy('currency:contact_list')

    def form_valid(self, form):
        response = super().form_valid(form)

        subject = 'ContactUs From Currency Project'
        message = f'''
        Subject From Client: {self.object.subject}
        Email: {self.object.email_from}
        Wants to contact
        '''

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [settings.EMAIL_HOST_USER],
            fail_silently=False,
        )

        return response


class UserProfileView(LoginRequiredMixin, generic.UpdateView):
    queryset = get_user_model().objects.all()
    template_name = 'my_profile.html'
    success_url = reverse_lazy('index')
    fields = (
        'first_name',
        'last_name',
    )

    def get_object(self, queryset=None):
        return self.request.user
