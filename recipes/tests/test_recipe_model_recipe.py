from .test_recipe_base_data import TestRecipeBaseData
from recipes.models import User, Category, Recipe
from django.core.exceptions import ValidationError
from parameterized import parameterized

class TestModelRecipe(TestRecipeBaseData):
    def setUp(self):
        self.recipe = self.make_recipe()

    def make_recipe_with_no_fields_by_default(
        self,
        title = "minha nova receita",
        description = "receita rapida",
        slug = "minha-nova-receita",
        preparation_time = 10,
        preparation_time_unit = "minutos",
        servings = 3,
        servings_unit = "porções",
        preparation_steps = "passos de preparo",
        category_name = "nova categoria",
        author_name = "novo usuario"
    ):
        recipe = Recipe(
            title = title,
            description = description,
            slug = slug,
            preparation_time = preparation_time,
            preparation_time_unit = preparation_time_unit,
            servings = servings,
            servings_unit = servings_unit,
            preparation_steps = preparation_steps,
            category = self.make_category(name=category_name),
            author = self.make_author(username=author_name)
        )
        return recipe

    @parameterized.expand(
            [
                ("title", 65),
                ("description", 165),
                ("preparation_time_unit", 65),
                ("servings_unit", 65)
            ]
    )
    def test_model_recipe_raises_error_if_size_of_title_is_greater_than_65_chars(self, field, length):
        setattr(self.recipe, field, "a" * (length + 1))
        was_validate_correctly = False
        try:
            self.recipe.clean_fields()
            self.recipe.save()
        except ValidationError:
            was_validate_correctly = True
        finally:
            assert was_validate_correctly

    @parameterized.expand(
            [
                ("is_published"),
                ("preparation_steps_is_html")
            ]
    )
    def test_model_recipe_some_fields_is_false_by_default(self, field):
        recipe = self.make_recipe_with_no_fields_by_default(
            title="minha receita sem setar campos default",
            author_name="meu novo usuario"
        )

        self.assertFalse(getattr(recipe, field))

    def test_model_recipe_str_representation_is_the_same_as_the_title_recipe(self):
        recipe = self.make_recipe_with_no_fields_by_default(
            title="minha receita sem setar campos default",
            author_name="meu novo usuario"
        )

        self.assertEqual(str(recipe), recipe.title)