from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def index(request: HttpRequest) -> HttpResponse:
    data: dict[str, object] = {
        "title": "Главная страница",
    }
    return render(request, "main/index.html", data)


def contacts(request: HttpRequest) -> HttpResponse:
    return render(request, "main/contacts.html")
