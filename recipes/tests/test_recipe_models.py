from .test_recipe_base_data import TestRecipeBaseData
from recipes.models import User, Category, Recipe
from django.core.exceptions import ValidationError
import pytest

class TestModelRecipe(TestRecipeBaseData):
    def setUp(self):
        self.recipe = self.make_recipe()

    def test_model_recipe_raises_error_if_size_of_title_is_greater_than_65_chars(self, field, length):
        self.recipe.title = "a" * 70
        was_validate_correctly = False
        try:
            self.recipe.clean_fields()
            self.recipe.save()
        except ValidationError:
            was_validate_correctly = True
        finally:
            assert was_validate_correctly