from django.urls import path
from . import views
from django.http import HttpResponse

urlpatterns = [
    path('', views.home, name="home"),
    path('recipe/<int:recipe_id>/', views.recipe_details, name="recipe"),
    path('recipes/category/<int:category_id>/', views.category_recipes, name="category"),
    path('recipes/search/', views.recipes_search, name="search")
]