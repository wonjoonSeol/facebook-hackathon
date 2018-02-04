from django.shortcuts import render
from django.http import HttpResponse
from .db import get_matches_for

def index(request):
    return render(request, 'learnapp/index.html')

def bio(request):
    return render(request, 'learnapp/bio.html')

def swipe(request):
    matches = get_matches_for('patrick.hainge@kcl.ac.uk')
    data = request.POST.get('password')
    print(data)
    return render(request, 'learnapp/swipe.html', {'matches': matches})

def module(request):
    return render(request, 'learnapp/module.html')

def register(request):
    return render(request, 'learnapp/register.html')
