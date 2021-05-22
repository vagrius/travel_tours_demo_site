import random

from django.http import HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import render

from data import departures, description, subtitle, title, tours


def get_context(pk):  # функция получения общего для разных страниц контекста из data.py по ключу
    context = {
               'key': pk,
               'title': tours[pk]['title'],
               'description': tours[pk]['description'],
               'short_description': f"{tours[pk]['description'][:80]}...",
               'departure': tours[pk]['departure'],
               'departure_ru': departures[tours[pk]['departure']].replace('И', 'и', 1),
               'picture': tours[pk]['picture'],
               'price': tours[pk]['price'],
               'stars': range(int(tours[pk]['stars'])),
               'stars_count': tours[pk]['stars'],
               'country': tours[pk]['country'],
               'nights': tours[pk]['nights'],
               'date': tours[pk]['date'],
               }
    return context


def add_to_context_extra(context):  # функция добавления к контексту некоторых дополнительных данных
    context['departures_list'] = departures
    context['base_info'] = [title, subtitle, description]
    return context


def main_view(request):
    pks = []  # формируем список из 6 неповторяющихся id туров
    while len(pks) < 6:
        pk = random.randint(1, len(tours))
        if pk not in pks:
            pks.append(pk)

    context_main = {'tours': []}  # формируем контекст состоящий из информации по 6 случайным турам
    for pk in pks:
        context = get_context(pk)
        context_main['tours'].append(context)

    context_main = add_to_context_extra(context_main)

    return render(request, "index.html", context=context_main)


def departure_view(request, departure):

    if departure not in departures:
        return HttpResponseNotFound(f"Направление с идентификатором '{departure}' не найдено!")

    price_list, nights_list = [], []
    context_main = {'tours': []}  # формируем контекст, выбирая данные по departure
    for pk in range(1, len(tours) + 1):
        context = get_context(pk)
        if context['departure'] == departure:
            context_main['tours'].append(context)
            price_list.append(context['price'])
            nights_list.append(context['nights'])

    context_main['agg'] = ({'min_price': min(price_list),  # добавляем данные по мин/макс ценам и кол-вам ночей
                            'max_price': max(price_list),
                            'min_nights': min(nights_list),
                            'max_nights': max(nights_list)})

    context_main = add_to_context_extra(context_main)

    return render(request, "departure/departure.html", context=context_main)


def tour_view(request, pk):

    if pk > len(tours):
        return HttpResponseNotFound(f"Тур с id={pk} не найден!")

    context_main = add_to_context_extra(get_context(pk))

    return render(request, "tour/tour.html", context=context_main)


def custom_handler404(request, exception):
    return HttpResponseNotFound('Ошибка 404: страница не найдена!')


def custom_handler500(request):
    return HttpResponseServerError('Ошибка 500: ошибка сервера!')
