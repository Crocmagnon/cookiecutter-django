from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Default custom user model for {{ cookiecutter.project_name }}."""
