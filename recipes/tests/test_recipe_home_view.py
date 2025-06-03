from django.urls import reverse, resolve
from recipes import views
from .test_recipe_base_data import TestRecipeBaseData

class RecipeHomeViewTest(TestRecipeBaseData):
    def test_recipe_home_view_function_is_correct(self):
        view = resolve(reverse("home"))
        self.assertIs(view.func, views.home)
# -----------------------

    def test_recipe_home_view_ruturns_status_code_200(self):
        response = self.client.get(reverse("home"))
        assert response.status_code == 200

    def test_recipe_home_view_render_page_home(self):
        response = self.client.get(reverse("home"))
        assert response.status_code == 200
        assert response.templates[0].name == "home.html"

    def test_recipe_home_template_shows_message_if_no_recipes_are_founded(self):
        response = self.client.get(reverse("home"))
        assert "Não existem receitas publicadas ainda" in response.content.decode("utf-8")

    def test_recipe_home_template_shows_recipe_cards(self):
        self.make_recipe()
        response = self.client.get(reverse("home"))
        content = response.content.decode("utf-8")
        assert "minha nova receita" in content
    
    def test_recipe_home_template_shows_message_if__no_recipes_is_published(self):
        self.make_recipe(
            title="minha receita não publicada",
            is_published=False
        )
        response = self.client.get(reverse("home"))
        assert "Não existem receitas publicadas ainda" in response.content.decode("utf-8")