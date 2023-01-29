import pytest
from django.core.management import call_command


@pytest.fixture(scope="session", autouse=True)
def _collectstatic():
    call_command("collectstatic", "--clear", "--noinput", "--verbosity=0")
