from django.shortcuts import render
from django.http import HttpResponse, Http404


from . models import Table

# Create your views here.
def index(request):
    return render(request, "singlepage/index.html")


texts = ["111",
         "222",
         "333",
         "444", ]


def section(request, num):
    if 1 <= num <= 4 or num == 'undefined':
        return HttpResponse(texts[num - 1])
    else:
        raise Http404("No such section")



from django.http import JsonResponse

def post_list(request):
   if request.method == "POST":
      name = request.POST.get('name')
      law = request.POST.get('law')
      argument = request.POST.get('argument')
      reset = request.POST.get('reset')
      # num1 = request.POST.get('num_1')
      # num2 = request.POST.get('num_2')
      # result = int(num1) + int(num2)
      result = name

   #    return JsonResponse({"result": result})
   #
   # else:
      return render(request, 'singlepage/index.html', context={"result":result})


# def checkout(request):
#     checks = request.POST.getlist('checks')
#     print(checks)  # Проверяем наличие id галочек
#     array_num = [int(item) for item in checks]  # перевод в числовой вид из стрингового представления
#     appen = []
#     flag = False  # флаг для определения 2 и более выбранных элементов (для if-else в HTML-шаблоне)
#     if (len(array_num) > 1):
#         for el in range(0, len(array_num)):
#             flag = True
#             count = array_num[el]  # получение значения первого элемента листа
#             chk = MenuShow.objects.get(id=count)  # выбираем из БД значение, равное id объекта в БД
#             print(chk)
#             appen.append(chk)  # присоединение к массиву для вывода двух и более галочек в итоговой таблице
#         checks_list = appen
#     else:
#         checks_list = MenuShow.objects.get(id=array_num[0])
#         flag = False
#         print(checks_list)
#     print(appen)
#     return render(request, './checkout.html', {'checks': checks, 'checks_list': checks_list, 'flag': flag})