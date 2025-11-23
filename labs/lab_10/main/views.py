from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def index(request: HttpRequest) -> HttpResponse:
    return render(request, "main/index.html")


def about(request: HttpRequest) -> HttpResponse:
    return render(request, "main/about.html")
