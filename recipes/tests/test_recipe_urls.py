from django.test import TestCase
from django.urls import reverse

class RecipeURLsTest(TestCase):
    def test_recipe_home_url_is_correct(self):
        home_url = reverse("home")
        assert home_url == "/"

    def test_recipe_category_url_is_correct(self):
        category_url = reverse("category", kwargs={"category_id":1})
        assert category_url == "/recipes/category/1/"

    def test_recipe_recipe_url_is_correct(self):
        category_url = reverse("recipe", kwargs={"recipe_id":1})
        assert category_url == "/recipe/1/"