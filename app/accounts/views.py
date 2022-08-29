from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import generic

from accounts.forms import SignUpForm


class SignUpView(generic.CreateView):
    queryset = get_user_model().objects.all()
    template_name = 'signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('accounts:signup_done')


class SignUPDoneView(generic.TemplateView):
    template_name = 'signup_done.html'


class UserActivateView(generic.RedirectView):
    pattern_name = 'index'

    def get(self, request, *args, **kwargs):
        username = kwargs.pop('username')
        user = get_object_or_404(get_user_model(), username=username)

        if user.is_active:
            pass
        else:
            user.is_active = True
            user.save()
        response = super().get(request, *args, **kwargs)
        return response
