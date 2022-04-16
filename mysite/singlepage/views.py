from django.shortcuts import render
from django.http import HttpResponse, Http404

from .models import Table


# Create your views here.
def index(request):

    post_list(request)
    return render(request, "singlepage/index.html", )


def post_list(request):
    if request.method == "POST":
        column_selection = request.POST.get('column_selection')
        condition_selection = request.POST.get('condition_selection')
        value_to_filter = request.POST.get('value_to_filter')
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

        result = []
        for i in range(len(queryset)):
            date, name, amount, distance = str(queryset[i]).split()
            table_row = f"""
                <tr class="table__row">
                <td class="table__down">{date}</td>
                <td class="table__down">{name}</td>
                <td class="table__down">{amount}</td>
                <td class="table__down">{distance}</td></tr>
                """
            result += table_row

        return HttpResponse(result)
