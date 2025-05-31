from .test_recipe_base_data import TestRecipeBaseData

class TestModelCategory(TestRecipeBaseData):
    def test_category_model_str_representation_if_is_the_same_as_the_category_name(self):
        category = self.make_category()
        self.assertEqual(str(category), category.name)