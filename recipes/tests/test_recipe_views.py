from django.urls import reverse, resolve
from recipes import views
from .test_recipe_base_data import TestRecipeBaseData

class RecipeViewsTest(TestRecipeBaseData):
    def test_recipe_home_view_function_is_correct(self):
        view = resolve(reverse("home"))
        self.assertIs(view.func, views.home)
    
    def test_recipe_recipe_view_function_is_correct(self):
        view = resolve(reverse("recipe",kwargs={"recipe_id":1}))
        self.assertIs(view.func, views.recipe_details)
    
    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse("category",kwargs={"category_id":1}))
        self.assertIs(view.func, views.category_recipes)
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


# -----------------------
    # ainda não irá retornar 200 pois não existe nada no banco de dados de teste
    def test_recipe_details_view_returns_status_code_200(self):
        self.make_recipe()
        response = self.client.get(reverse("recipe", kwargs={"recipe_id":1}))
        assert response.status_code == 200

    def test_recipe_details_view_returns_status_code_404(self):
        self.make_recipe()
        response = self.client.get(reverse("recipe", kwargs={"recipe_id":1000}))
        assert response.status_code == 404

    #ainda não passou pq a função de details só retorna uma mensagem junto com o status 404
    def test_recipe_details_view_render_recipes_page(self):
        self.make_recipe()
        response = self.client.get(reverse("recipe", kwargs={"recipe_id":1}))
        assert response.templates[0].name == "recipes_view.html"

    def test_recipe_details_template_shows_recipe_card_details(self):
        self.make_recipe()
        response = self.client.get(reverse("home"))
        content = response.content.decode("utf-8")
        assert "minha nova receita" in content
        assert "receita rapida" in content

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