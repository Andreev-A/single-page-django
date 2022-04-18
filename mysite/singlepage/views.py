from django.shortcuts import render
from django.http import HttpResponse, Http404
from .models import Table

NUMBER_OF_TABLE_ROW = 7
_form_data = (None, None, None)
_page = 1


# Create your views here.
def index(request):
    return render(request, "singlepage/index.html")


def fetch_from_database(form_data):
    """
    Receiving and filtering data  from MySQL.
    """
    column_selection, condition_selection, value_to_filter = form_data
    data = []
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
    for i in range(len(queryset)):
        data.append(str(queryset[i]).split())
    return data


def table_body_output(form_data, page_navigation):
    """
    Forming the table body in HTML page by page.
    """
    global _page
    data = fetch_from_database(form_data)
    number_of_pages = len(data) // NUMBER_OF_TABLE_ROW + 1 \
        if not data or len(data) % NUMBER_OF_TABLE_ROW else len(data) // NUMBER_OF_TABLE_ROW
    if page_navigation == -1 and _page > 1:
        _page += page_navigation
    elif page_navigation == 1 and _page < number_of_pages:
        _page += page_navigation
    elif not page_navigation:
        _page = 1
    result = []
    start = NUMBER_OF_TABLE_ROW * _page - NUMBER_OF_TABLE_ROW
    stop = NUMBER_OF_TABLE_ROW * _page
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
               <th colspan="4">Страница {_page} из {number_of_pages}</th></tr>
               """
    return result


def post_list(request):
    """
    Getting form data. Return of the first page.
    """
    global _form_data
    if request.method == "POST":
        column_selection = request.POST.get('column_selection')
        condition_selection = request.POST.get('condition_selection')
        value_to_filter = request.POST.get('value_to_filter')
        _form_data = column_selection, condition_selection, value_to_filter
        page_navigation = 0
        result = table_body_output(_form_data, page_navigation)
        return HttpResponse(result)
    else:
        raise Http404("Bad request")


def section(request, num):
    """
    Page navigation. Return the selected page.
    """
    global _form_data
    if 0 <= num <= 3:
        page_navigation = 0
        if num in (0, 1):
            _form_data = (None, None, None)
        elif num == 2:
            page_navigation = -1
        elif num == 3:
            page_navigation = 1
        result = table_body_output(_form_data, page_navigation)
        return HttpResponse(result)
    else:
        raise Http404("Bad request")
