from django.shortcuts import render
from django.http import HttpResponse
from .db import get_matches_for, get_instructor

def index(request):
    return render(request, 'learnapp/index.html')

def bio(request, id):
    instructor_obj = get_instructor(id)
    return render(request, 'learnapp/bio.html', {'data': instructor_obj})

def swipe(request):
    matches = get_matches_for('patrick.hainge@kcl.ac.uk')
    return render(request, 'learnapp/swipe.html', {'matches': matches})

def module(request):
    return render(request, 'learnapp/module.html')

def register(request):
    return render(request, 'learnapp/register.html')
