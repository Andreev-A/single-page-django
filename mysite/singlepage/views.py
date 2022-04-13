from django.shortcuts import render
from django.http import HttpResponse, Http404


# Create your views here.
def index(request):
    return render(request, "singlepage/index.html")


texts = ["111",
         "222",
         "333",
         "444", ]


def section(request, num):
    if 1 <= num <= 4:
        return HttpResponse(texts[num - 1])
    else:
        raise Http404("No such section")
