from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def main(request: HttpRequest) -> HttpResponse:
    data: dict[str, object] = {
        "title": "Главная",
        "header": "Привет! Я — R8Zorg",
    }
    return render(request, "main/main.html", data)


def contacts(request: HttpRequest) -> HttpResponse:
    return render(request, "main/contacts.html")
