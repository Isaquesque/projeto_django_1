from .test_recipe_base_data import TestRecipeBaseData
from recipes.models import User, Category, Recipe
from django.core.exceptions import ValidationError
from parameterized import parameterized

class TestModelRecipe(TestRecipeBaseData):
    def setUp(self):
        self.recipe = self.make_recipe()
        
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