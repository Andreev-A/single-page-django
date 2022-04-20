from django.shortcuts import render
from django.http import HttpResponse, Http404
from .models import Table

NUMBER_OF_TABLE_ROW = 7
_dataset_from_database = []
_page = 1


# Create your views here.
def index(request):
    return render(request, "singlepage/index.html")


def fetch_from_database(form_data):
    """
    Receiving and filtering data  from MySQL.
    """
    column_selection, condition_selection, value_to_filter = form_data
    dataset = []
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
    for data in queryset:
        dataset.append(str(data).split())
    return dataset


def table_body_output(dataset, page_navigation):
    """
    Forming the table body in HTML page by page.
    """
    global _page
    table_rows = []
    number_of_pages = len(dataset) // NUMBER_OF_TABLE_ROW + 1 \
        if not dataset or len(dataset) % NUMBER_OF_TABLE_ROW else len(dataset) // NUMBER_OF_TABLE_ROW
    if page_navigation == -1 and _page > 1:
        _page += page_navigation
    elif page_navigation == 1 and _page < number_of_pages:
        _page += page_navigation
    elif not page_navigation:
        _page = 1
    start = NUMBER_OF_TABLE_ROW * _page - NUMBER_OF_TABLE_ROW
    stop = NUMBER_OF_TABLE_ROW * _page
    for data in dataset[start:stop]:
        date, name, amount, distance = data
        table_row = f"""
                     <tr class="table__row">
                     <td class="table__down">{date}</td>
                     <td class="table__down">{name}</td>
                     <td class="table__down">{amount}</td>
                     <td class="table__down">{distance}</td></tr>
                     """
        table_rows += table_row
    table_rows += f"""
               <tr class="table__row">
               <th colspan="4">Страница {_page} из {number_of_pages}</th></tr>
               """
    return table_rows


def post_list(request):
    """
    Getting form data. Return of the first page.
    """
    global _dataset_from_database
    if request.method == "POST":
        column_selection = request.POST.get('column_selection')
        condition_selection = request.POST.get('condition_selection')
        value_to_filter = request.POST.get('value_to_filter')
        form_data = column_selection, condition_selection, value_to_filter
        _dataset_from_database = fetch_from_database(form_data)
        page_navigation = 0
        table_rows = table_body_output(_dataset_from_database, page_navigation)
        return HttpResponse(table_rows)
    else:
        raise Http404("Bad request")


def section(request, num):
    """
    Page navigation. Return the selected page.
    """
    global _dataset_from_database
    if 1 <= num <= 3:
        page_navigation = 0
        if num == 1:
            form_data = (None, None, None)
            _dataset_from_database = fetch_from_database(form_data)
        elif num == 2:
            page_navigation = -1
        elif num == 3:
            page_navigation = 1
        table_rows = table_body_output(_dataset_from_database, page_navigation)
        return HttpResponse(table_rows)
    else:
        raise Http404("Bad request")
