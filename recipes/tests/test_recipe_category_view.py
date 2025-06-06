from django.urls import reverse, resolve
from recipes import views
from .test_recipe_base_data import TestRecipeBaseData
from .test_pagination_helper import TestPaginationHelper

class TestRecipeCategoryView(TestRecipeBaseData):
    
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

class TestRecipeCategoryViewPagination(TestPaginationHelper):

    def test_category_view_pagination_for_initial_page(self):
        self.make_recipes(
            [
                {
                    "category":"categoria1",
                    "author":"name1",
                    "qty_recipes": 24,
                    "published":True
                }
            ]
        )

        response = self.client.get(reverse("category", kwargs={"category_id":1}), query_params={"page":1})
        self.validate_pagination_view_state(
            response,
            pagination_list=[1,2,3,4],
            current_page=1,
            per_page=6,
            first_page=1,
            last_page=4,
            first_page_is_in_range=True,
            last_page_is_in_range=True,
            has_more_than_one_page=True
        )
            
    def test_category_view_pagination_for_intermediary_page(self):
        self.make_recipes(
            [
                {
                    "category":"categoria1",
                    "author":"name1",
                    "qty_recipes": 50,
                    "published":True
                }
            ]
        )
        
        response = self.client.get(reverse("category", kwargs={"category_id":1}), query_params={"page":4})
        self.validate_pagination_view_state(
            response,
            pagination_list=[3,4,5,6],
            current_page=4,
            per_page=6,
            first_page=1,
            last_page=9,
            first_page_is_in_range=False,
            last_page_is_in_range=False,
            has_more_than_one_page=True
        )
            
    def test_category_view_pagination_for_final_page(self):
        self.make_recipes(
            [
                {
                    "category":"categoria1",
                    "author":"name1",
                    "qty_recipes": 42,
                    "published":True
                }
            ]
        )

        response = self.client.get(reverse("category", kwargs={"category_id":1}), query_params={"page":7})
        self.validate_pagination_view_state(
            response,
            pagination_list=[4,5,6,7],
            current_page=7,
            per_page=6,
            first_page=1,
            last_page=7,
            first_page_is_in_range=False,
            last_page_is_in_range=True,
            has_more_than_one_page=True
        )

    def test_category_view_pagination_for_non_existent_page(self):
        self.make_recipes(
            [
                {
                    "category":"categoria1",
                    "author":"name1",
                    "qty_recipes": 24,
                    "published":True
                }
            ]
        )

        response = self.client.get(reverse("category", kwargs={"category_id":1}), query_params={"page":5})
        self.assertEqual(response.status_code, 404)
    
    def test_category_view_pagination_for_few_recipes(self):
        self.make_recipes(
            [
                {
                    "category":"categoria1",
                    "author":"name1",
                    "qty_recipes": 5,
                    "published":True
                }
            ]
        )

        response = self.client.get(reverse("category", kwargs={"category_id":1}), query_params={"page":1})
        self.validate_pagination_view_state(
            response,
            pagination_list=[1],
            current_page=1,
            per_page=5,
            first_page=1,
            last_page=1,
            first_page_is_in_range=True,
            last_page_is_in_range=True,
            has_more_than_one_page=False
        )

    def test_category_view_pagination_for_invalid_page(self):
        self.make_recipes(
            [
                {
                    "category":"categoria1",
                    "author":"name1",
                    "qty_recipes": 24,
                    "published":True
                }
            ]
        )

        response = self.client.get(reverse("category", kwargs={"category_id":1}), query_params={"page":"abc"})
        self.validate_pagination_view_state(
            response,
            pagination_list=[1,2,3,4],
            current_page=1,
            per_page=6,
            first_page=1,
            last_page=4,
            first_page_is_in_range=True,
            last_page_is_in_range=True,
            has_more_than_one_page=True
        )