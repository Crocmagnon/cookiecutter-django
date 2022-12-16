import django_registration.forms

from common.models import User


class RegistrationForm(django_registration.forms.RegistrationForm):
    class Meta(django_registration.forms.RegistrationForm.Meta):
        model = User
