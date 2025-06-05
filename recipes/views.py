from django.shortcuts import render
from django.http import HttpResponse
from utils.fake_data_generator import DataGenerator
from .models import Recipe, Category
from django.db.models import Q
from django.core.paginator import Paginator
from utils.make_pagination import make_pagination

def home(request):
    all_recipes = list(Recipe.objects.all().filter(is_published = True))

    pagination_dict = make_pagination(
        request,
        all_recipes,
        qty_items_per_page = 6,
        num_pages = 4,
        num_pages_before_current_page = 1,
        num_pages_after_current_page = 2
    )

    return render(request, "home.html", context=pagination_dict)

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

        pagination_dict = make_pagination(
            request,
            recipes,
            qty_items_per_page=6,
            num_pages=4,
            num_pages_before_current_page=1,
            num_pages_after_current_page=2
        )

        context = pagination_dict
        context["category_name"] = category_name
    else:
        return HttpResponse(content="Categoria não encontrada", status=404)

    return render(request, "category_view.html", context)

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

        pagination_dict = make_pagination(
            request,
            recipes,
            qty_items_per_page=6,
            num_pages=4,
            num_pages_before_current_page=1,
            num_pages_after_current_page=2
        )

        context = pagination_dict
        context["search_term"] = search_term
        context["search_string"] = f'&search={search_term}'

        return render(request, "search.html", context=context)
    
    return HttpResponse("nenhum termo correspondente foi encontrado", status=404)