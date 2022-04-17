from django.shortcuts import render
from django.http import HttpResponse
from .models import Table

FORM_DATA = (None, None, None)
PAGE = 1


# Create your views here.
def index(request):
    return render(request, "singlepage/index.html")


def table_body_output(FORM_DATA, PAGE):
    global NUMBER_OF_PAGES
    column_selection, condition_selection, value_to_filter = FORM_DATA
    if column_selection == 'name' and condition_selection in ('equal', 'contains'):
        queryset = Table.objects.filter(name=value_to_filter)
    elif column_selection == 'name' and condition_selection == 'larger':
        queryset = Table.objects.filter(name__gt=value_to_filter)
    elif column_selection == 'name' and condition_selection == 'smaller':
        queryset = Table.objects.filter(name__lt=value_to_filter)
    elif column_selection == 'amount' and condition_selection in ('equal', 'contains'):
        queryset = Table.objects.filter(amount=value_to_filter)
    elif column_selection == 'amount' and condition_selection == 'larger':
        queryset = Table.objects.filter(amount__gt=value_to_filter)
    elif column_selection == 'amount' and condition_selection == 'smaller':
        queryset = Table.objects.filter(amount__lt=value_to_filter)
    elif column_selection == 'distance' and condition_selection in ('equal', 'contains'):
        queryset = Table.objects.filter(distance=value_to_filter)
    elif column_selection == 'distance' and condition_selection == 'larger':
        queryset = Table.objects.filter(distance__gt=value_to_filter)
    elif column_selection == 'distance' and condition_selection == 'smaller':
        queryset = Table.objects.filter(distance__lt=value_to_filter)
    else:
        queryset = Table.objects.all()

    data = []
    for i in range(len(queryset)):
        data.append(str(queryset[i]).split())
    NUMBER_OF_PAGES = len(data) // 7 + 1 if not data or len(data) % 7 else len(data) // 7
    result = []
    start = 7 * PAGE - 7
    stop = 7 * PAGE
    for el in data[start:stop]:
        date, name, amount, distance = el
        table_row = f"""
                    <tr class="table__row">
                    <td class="table__down">{date}</td>
                    <td class="table__down">{name}</td>
                    <td class="table__down">{amount}</td>
                    <td class="table__down">{distance}</td></tr>
                    """
        result += table_row
    result += f"""
            <tr class="table__row">
            <th colspan="4">Страница {PAGE} из {NUMBER_OF_PAGES}</th></tr>
            """
    return result


def post_list(request):
    global FORM_DATA
    if request.method == "POST":
        column_selection = request.POST.get('column_selection')
        condition_selection = request.POST.get('condition_selection')
        value_to_filter = request.POST.get('value_to_filter')
        FORM_DATA = column_selection, condition_selection, value_to_filter
        PAGE = 1
        result = table_body_output(FORM_DATA, PAGE)
        return HttpResponse(result)


def section(request, num):
    global FORM_DATA
    global PAGE
    if 0 <= num <= 3:
        if num in (0, 1):
            FORM_DATA = (None, None, None)
            PAGE = 1
        if num == 2 and PAGE > 1:
            PAGE -= 1
        elif num == 3 and PAGE < NUMBER_OF_PAGES:
            PAGE += 1
        result = table_body_output(FORM_DATA, PAGE)
        return HttpResponse(result)
