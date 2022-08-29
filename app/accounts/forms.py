import uuid

from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model, password_validation
from django.core.mail import send_mail
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class SignUpForm(forms.ModelForm):
    username = forms.CharField(label='Enter Username', min_length=4, max_length=150)
    email = forms.EmailField(label='Enter email')
    password1 = forms.CharField(label='Enter password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = get_user_model()
        fields = (
            'username',
            'email',
        )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        return username.lower()

    def clean_email(self):
        email = self.cleaned_data.get("email")
        return email.lower()

    def clean(self):
        cleaned_data = super().clean()
        if not self.errors:
            if cleaned_data['password1'] != cleaned_data['password2']:
                raise forms.ValidationError('Passwords missmatch!')

        return cleaned_data

    def _post_clean(self):
        super()._post_clean()

        password = self.cleaned_data.get("password2")
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except ValidationError as error:
                self.add_error("password2", error)

    def save(self, commit=True):
        instance: User = super().save(commit=False)
        instance.username = str(uuid.uuid4())
        instance.is_active = False
        instance.set_password(self.cleaned_data['password1'])

        if commit:
            instance.save()

        self._send_activation_email()

        return instance

    def _send_activation_email(self):
        subject = 'Activate your account'
        body = f'''
        Activation link: {settings.HTTP_SCHEMA}://{settings.DOMAIN}{reverse('accounts:user_activate',
                                                                            args=(self.instance.username, ))}
        '''

        send_mail(
            subject,
            body,
            settings.EMAIL_HOST_USER,
            [self.instance.email],
            fail_silently=False,
        )

