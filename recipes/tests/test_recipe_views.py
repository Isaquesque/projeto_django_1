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

    def test_recipe_search_view_function_is_correct(self):
        resolved_url = resolve(reverse("search"))
        self.assertIs(resolved_url.func, views.recipes_search)
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
        response = self.client.get(reverse("recipe" , kwargs={"recipe_id":1}))
        content = response.content.decode("utf-8")
        assert "minha nova receita" in content
    
    def test_recipe_details_view_returns_404_code_if_the_recipe_are_no_published(self):
        self.make_recipe(
            title="minha recieta não publicada",
            is_published=False
        )
        response = self.client.get(reverse("recipe" , kwargs={"recipe_id":1}))
        content = response.content.decode("utf-8")
        assert "minha nova receita" not in content
        assert response.status_code == 404

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
    
# -----------------------

    def test_recipe_search_view_returns_status_code_200(self):
        search_url = f'{reverse("search")}?search=teste'
        response = self.client.get(search_url)
        self.assertEqual(response.status_code, 200)

    def test_recipe_search_view_render_search_page(self):
        search_url = f'{reverse("search")}?search=teste'
        response = self.client.get(search_url)
        self.assertEqual(response.templates[0].name, "search.html")

    def test_recipe_search_view_returns_status_code_404_if_there_is_no_matching_search(self):
        response = self.client.get(reverse("search"))
        self.assertEqual(response.status_code, 404)