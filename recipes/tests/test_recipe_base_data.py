from django.test import TestCase
from recipes.models import User,Category,Recipe

class TestRecipeBaseData(TestCase):
    def make_author(
        self,
        username="username",
        email="email@gmail.com",
        password="123456",
        first_name="name",
        last_name="lastname"
    ):
            
        user_data = {
            "username": username,
            "email": email,
            "password": password,
            "first_name": first_name,
            "last_name": last_name
        }
        return  User.objects.create_user(**user_data)
    
    def make_category(self, name="categoriaTeste"):
         return Category.objects.create(name=name)
    
    def make_recipe(
        self,
        title = "minha nova receita",
        description = "receita rapida",
        slug = "minha-nova-receita",
        preparation_time = 10,
        preparation_time_unit = "minutos",
        servings = 3,
        servings_unit = "porções",
        preparation_steps = "passos de preparo",
        preparation_steps_is_html = False,
        is_published = True,
        category = {},
        author = {}
    ):
        recipe_data = {
            "title": title,
            "description": description,
            "slug": slug,
            "preparation_time": preparation_time,
            "preparation_time_unit": preparation_time_unit,
            "servings": servings,
            "servings_unit": servings_unit,
            "preparation_steps": preparation_steps,
            "preparation_steps_is_html": preparation_steps_is_html,
            "is_published": is_published,
            "category": self.make_category(**category),
            "author": self.make_author(**author)
        }

        return Recipe.objects.create(**recipe_data)