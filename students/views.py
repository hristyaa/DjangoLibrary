import http

from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def example_view(request):
    return render(request, 'app/example.html')


def show_data(request):
    if request.method == 'GET':
        return render(request, 'app/show_data.html')


def submit_data(request):
    request.GET
    request.POST
    if request.method == 'POST':
        return HttpResponse('Данные отправлены')


def show_item(request, item_id):
     return render(request, 'app/item.html', {'item_id': item_id})
