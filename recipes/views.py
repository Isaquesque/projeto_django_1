from django.shortcuts import render
from django.http import HttpResponse
from utils.fake_data_generator import DataGenerator
from .models import Recipe, Category
from django.db.models import Q

def home(request):
    recipes = list(Recipe.objects.all().filter(is_published = True))

    return render(request, "home.html", context={"recipes":recipes})

def recipe_details(request, recipe_id):
    recipe = Recipe.objects.filter(id=recipe_id, is_published = True)

    if(recipe):
        recipe = recipe[0]
    else:
        return HttpResponse(content="Receita não encontrada", status=404)

    return render(request, "recipes_view.html", context={"recipe":recipe})

def category_recipes(request, category_id):
    category_name = Category.objects.filter(id=category_id)
    recipes = list(Recipe.objects.filter(category__id = category_id, is_published = True))
    

    if(category_name):
        category_name = category_name[0].name
    else:
        return HttpResponse(content="Categoria não encontrada", status=404)

    return render(request, "category_view.html", context={"recipes":recipes, "category_name":category_name})

def recipes_search(request):
    params = request.GET
    search_term = params.get("search", "").strip()
    if(search_term):
        recipes = Recipe.objects.filter(
            Q(
                Q(title__icontains = search_term) | Q(description__icontains = search_term)
            ),
            is_published = True
        )
        return render(request, "search.html", context={"search_term":search_term, "recipes":recipes})
    
    return HttpResponse("nenhum termo correspondente foi encontrado", status=404)