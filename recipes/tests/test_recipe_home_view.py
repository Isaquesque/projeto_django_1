from django.urls import reverse, resolve
from recipes import views
from .test_recipe_base_data import TestRecipeBaseData
from .test_pagination_helper import TestPaginationHelper


class TestRecipeHomeView(TestRecipeBaseData):
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
# -----------------------

class TestRecipeHomeViewPagination(TestPaginationHelper):

    def test_home_view_pagination_for_initial_page(self):
        self.make_recipes(
            [
                {
                    "category":"categoria1",
                    "author":"name1",
                    "qty_recipes": 18,
                    "published":True
                }
            ]
        )

        response = self.client.get(reverse("home"), query_params={"page":1})
        self.validate_pagination_view_state(
            response,
            pagination_list=[1,2,3],
            current_page=2,
            per_page=6,
            first_page=1,
            last_page=3,
            first_page_is_in_range=True,
            last_page_is_in_range=True,
            has_more_than_one_page=True
        )
            
    def test_home_view_pagination_for_intermediary_page(self):
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
        
        response = self.client.get(reverse("home"), query_params={"page":4})
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
            
    def test_home_view_pagination_for_final_page(self):
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

        response = self.client.get(reverse("home"), query_params={"page":7})
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

    def test_home_view_pagination_for_non_existent_page(self):
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

        response = self.client.get(reverse("home"), query_params={"page":5})
        self.assertEqual(response.status_code, 404)
    
    def test_home_view_pagination_for_few_recipes(self):
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

        response = self.client.get(reverse("home"), query_params={"page":1})
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

    def test_home_view_pagination_for_invalid_page(self):
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

        response = self.client.get(reverse("home"), query_params={"page":"abc"})
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