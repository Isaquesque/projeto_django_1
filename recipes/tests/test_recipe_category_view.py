from django.urls import reverse, resolve
from recipes import views
from .test_recipe_base_data import TestRecipeBaseData

class RecipeCategoryViewTest(TestRecipeBaseData):
    
    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse("category",kwargs={"category_id":1}))
        self.assertIs(view.func, views.category_recipes)

# -----------------------
    # ainda não irá retornar 200 pois não existe nada no banco de dados de teste
    def test_recipe_category_view_returns_status_code_200(self):
        self.make_recipe()
        response = self.client.get(reverse("category", kwargs={"category_id":1}))
        assert response.status_code == 200

    def test_recipe_category_view_returns_status_code_404(self):
        self.make_recipe()
        response = self.client.get(reverse("category", kwargs={"category_id":1000}))
        assert response.status_code == 404

    #ainda não passou pq a função de category só retorna uma mensagem junto com o status 404
    def test_recipe_category_view_render_category_page(self):
        self.make_recipe()
        response = self.client.get(reverse("category", kwargs={"category_id":1}))
        assert response.templates[0].name == "category_view.html"

    def test_recipe_category_template_show_recipe_cards(self):
        self.make_recipe()
        response = self.client.get(reverse("category", kwargs={"category_id":1}))
        recipes = response.context[0]["recipes"]
        for recipe in recipes:
            assert recipe.title in response.content.decode("utf-8")

    def test_recipe_category_template_shows_message_if_no_recipes_are_created(self):
        self.make_category("minha categoria sem receitas")
        response = self.client.get(reverse("category", kwargs={"category_id":1}))
        assert "Não existem receitas publicadas nesta categoria ainda" in response.content.decode("utf-8")

    def test_recipe_category_template_shows_message_if__no_recipes_is_published(self):
        self.make_recipe(
            title="minha receita não publicada",
            is_published=False
        )
        response = self.client.get(reverse("category", kwargs={"category_id":1}))
        assert "Não existem receitas publicadas nesta categoria ainda" in response.content.decode("utf-8")