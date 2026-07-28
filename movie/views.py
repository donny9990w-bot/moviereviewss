from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request, 'home.html', {'name': 'Juan David Bedoya'})

def about(request):
    return HttpResponse("About")