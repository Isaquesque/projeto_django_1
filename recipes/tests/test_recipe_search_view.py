from django.urls import reverse, resolve
from recipes import views
from recipes.models import User, Category
from .test_recipe_base_data import TestRecipeBaseData
from .test_pagination_helper import TestPaginationHelper

class TestRecipeSearchView(TestRecipeBaseData):

    def test_recipe_search_view_function_is_correct(self):
        resolved_url = resolve(reverse("search"))
        self.assertIs(resolved_url.func, views.recipes_search)

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

    def test_recipe_search_template_shows_recipe_cards_searched(self):
        recipe1 = self.make_recipe(
            title="doce de leite",
            slug="doce-de-leite",
            description="Uma sobremesa rápida, refrescante e deliciosa.",
            author={
                "username":"joao", 
                "email":"joao@gmail.com"
            },
            category={
                "name":"sobremesa"
            }
        )

        recipe2 = self.make_recipe(
            title="macarrão com queijo",
            slug="macarrão-com-queijo",
            description="Um clássico brasileiro, receita rápida e prática.",
            author={
                "username":"pedro", 
                "email":"pedro@gmail.com"
            },
            category={
                "name":"almoço"
            }
        )

        recipe3 = self.make_recipe(
            title="sanduiche de frango",
            slug="sanduiche-de-frango",
            description="Uma opção leve e prática para o lanche.",
            author={
                "username":"carlos", 
                "email":"carlos@gmail.com"
            },
            category={
                "name":"lanche"
            }
        )
        response1 = self.client.get(reverse("search"), query_params={"search":"doce"})
        content1 = response1.content.decode("utf-8")
        self.assertIn("doce de leite", content1)
        self.assertNotIn("macarrão com queijo", content1)
        self.assertNotIn("sanduiche de frango", content1)

        response2 = self.client.get(reverse("search"), query_params={"search":"prática"})
        content2 = response2.content.decode("utf-8")
        self.assertIn("macarrão com queijo", content2)
        self.assertIn("sanduiche de frango", content2)
        self.assertNotIn("doce de leite", content2)

        response3 = self.client.get(reverse("search"), query_params={"search":"rápida"})
        content3 = response3.content.decode("utf-8")
        self.assertIn("doce de leite", content3)
        self.assertIn("macarrão com queijo", content3)
        self.assertNotIn("sanduiche de frango", content3)
        

    def test_recipe_search_template_shows_message_if_no_recipe_matches_the_search(self):
        response = self.client.get(reverse("search"), query_params={"search":"doce"})
        content = response.content.decode("utf-8")
        self.assertIn("Não existem receitas correspondentes a esta pesquisa.", content)

class TestRecipeSearchViewPagination(TestPaginationHelper):

    def make_recipes(self, category_info):
        for info in category_info:
            category = info["category"] if isinstance(info["category"],Category) else self.make_category(info["category"])
            author =   info["author"] if isinstance(info["author"],User) else self.make_author(info["author"])
            for i in range(info["qty_recipes"]):
                self.make_recipe(
                    title = info["title"],
                    slug = "-".join(info["title"].split(" "))+f"{i+1}",
                    is_published= info["published"],
                    author= author,
                    category= category
                )
        """
            category_info - ex: [{
                "title":"titulo1"
                "category": "name" | category
                "author" : "user" | User
                "qty_recipes": 5
                "published": True
            }]

            Você pode fornecer um nome em category para criar uma categoria com este nome,
            ou então pode fornecer diretamente uma instância de Category em category.

            Para author é da mesma maneira.

        """

    def test_search_view_pagination_for_initial_page(self):
        self.make_recipes(
            [
                {
                    "title":"meu titulo",
                    "category":"categoria1",
                    "author":"name1",
                    "qty_recipes": 24,
                    "published":True
                }
            ]
        )

        response = self.client.get(reverse("search"), query_params={"search":"meu titulo","page":1})
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
                    "title":"meu titulo",
                    "category":"categoria1",
                    "author":"name1",
                    "qty_recipes": 50,
                    "published":True
                }
            ]
        )
        
        response = self.client.get(reverse("search"), query_params={"search":"meu titulo","page":4})
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
                    "title":"meu titulo",
                    "category":"categoria1",
                    "author":"name1",
                    "qty_recipes": 42,
                    "published":True
                }
            ]
        )

        response = self.client.get(reverse("search"), query_params={"search":"meu titulo","page":7})
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
                    "title":"meu titulo",
                    "category":"categoria1",
                    "author":"name1",
                    "qty_recipes": 24,
                    "published":True
                }
            ]
        )

        response = self.client.get(reverse("search"), query_params={"search":"meu titulo","page":5})
        self.assertEqual(response.status_code, 404)
    
    def test_category_view_pagination_for_few_recipes(self):
        self.make_recipes(
            [
                {
                    "title":"meu titulo",
                    "category":"categoria1",
                    "author":"name1",
                    "qty_recipes": 5,
                    "published":True
                }
            ]
        )

        response = self.client.get(reverse("search"), query_params={"search":"meu titulo","page":1})
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
                    "title":"meu titulo",
                    "category":"categoria1",
                    "author":"name1",
                    "qty_recipes": 24,
                    "published":True
                }
            ]
        )

        response = self.client.get(reverse("search"), query_params={"search":"meu titulo","page":"abc"})
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
