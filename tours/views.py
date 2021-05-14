from django.shortcuts import render
from django.http import HttpResponseNotFound, HttpResponseServerError


def main_view(request):
    return render(request, "index.html")


def departure_view(request, departure):
    return render(request, "departure/departure.html")


def tour_view(request, id):
    return render(request, "tour/tour.html")


def custom_handler404(request):
    return HttpResponseNotFound('Страница не найдена!')


def custom_handler500(request):
    return HttpResponseServerError('Ошибка сервера!')
