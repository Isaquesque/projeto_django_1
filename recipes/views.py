from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request, "home.html")

def recipe_card(request, id):
    return render(request, "recipes_view.html")