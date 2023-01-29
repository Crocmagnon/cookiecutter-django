from django.conf import settings


def debug_toolbar_bypass_internal_ips(_) -> bool:
    """
    Display debug toolbar according to the DEBUG_TOOLBAR setting only.

    By default, DjDT is displayed according to an `INTERNAL_IPS` settings.
    This is impossible to predict in a docker/k8s environment so we bypass this check.
    """
    return settings.DEBUG_TOOLBAR
