from django.shortcuts import render
from django.http import HttpResponse
from utils.fake_data_generator import DataGenerator

def home(request):
    data_list = []
    for _ in range(6):
        data_list.append(DataGenerator.generate())

    return render(request, "home.html", context={"data_list":data_list})

def recipe_card(request, id):
    data = DataGenerator.generate()

    return render(request, "recipes_view.html", context={"data":data})