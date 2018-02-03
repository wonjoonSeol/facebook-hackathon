from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, 'learnapp/index.html')

def bio(request):
    return render(request, 'learnapp/bio.html')

def module(request):
    return render(request, 'learnapp/module.html')

def register(request):
    return render(request, 'learnapp/register.html')
