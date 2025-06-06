from django.test import TestCase
from recipes.models import User,Category,Recipe
from utils.fake_data_generator import DataGenerator

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
            "category": category if isinstance(category, Category) else self.make_category(**category),
            "author": author if isinstance(author, User) else self.make_author(**author)
        }

        return Recipe.objects.create(**recipe_data)
    
    def make_recipes(
        self, 
        category_info: list[dict]
    ):
        """
            category_info - ex: [{
                "category": "name" | category
                "author" : "user" | User
                "qty_recipes": 5
                "published": True
            }]

            Você pode fornecer um nome em category para criar uma categoria com este nome,
            ou então pode fornecer diretamente uma instância de Category em category.

            Para author é da mesma maneira.

        """
        for info in category_info:
            category = info["category"] if isinstance(info["category"],Category) else self.make_category(info["category"])
            author =   info["author"] if isinstance(info["author"],User) else self.make_author(info["author"])
            for i in range(info["qty_recipes"]):
                data = DataGenerator.generate()
                self.make_recipe(
                    title = data["title"],
                    slug = data["slug"] + f"-{i+1}",
                    is_published= info["published"],
                    author= author,
                    category= category
                )

