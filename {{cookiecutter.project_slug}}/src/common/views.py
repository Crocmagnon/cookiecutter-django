import random

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render


def hello_world(request: WSGIRequest) -> HttpResponse:
    context = {"value": random.randint(1, 1000)}  # noqa: S311
    if request.htmx:
        return render(request, "common/hello-random.html", context)
    return render(request, "common/base.html", context)
