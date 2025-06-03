from django.urls import reverse, resolve
from recipes import views
from .test_recipe_base_data import TestRecipeBaseData
from django.test import Client

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
