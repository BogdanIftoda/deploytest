# Create your views here.
from django.shortcuts import render


def home_view(request):
    return render(request, 'home/home.html')
