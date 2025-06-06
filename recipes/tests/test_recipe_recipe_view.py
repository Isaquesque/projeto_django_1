from django.urls import reverse, resolve
from recipes import views
from .test_recipe_base_data import TestRecipeBaseData

class TestRecipeRecipeView(TestRecipeBaseData):
    
    def test_recipe_recipe_view_function_is_correct(self):
        view = resolve(reverse("recipe",kwargs={"recipe_id":1}))
        self.assertIs(view.func, views.recipe_details)
    
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