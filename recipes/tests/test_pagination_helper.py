from .test_recipe_base_data import TestRecipeBaseData

class TestPaginationHelper(TestRecipeBaseData):
    def validate_pagination_view_state(self, 
        response,
        pagination_list: list[int],
        current_page: int,
        per_page: int,
        first_page: int,
        last_page: int,
        first_page_is_in_range: bool,
        last_page_is_in_range: bool,
        has_more_than_one_page: bool,
    ):
        content = response.content.decode("utf-8")
        context = response.context

        recipes_context = context["recipes"]
        list_context = context["pagination_list"]
        current_page_context = context["current_page"]
        first_page_context = context["first_page"]
        last_page_context = context["last_page"]
        first_page_is_in_range_context = context["first_page_is_in_range"]
        last_page_is_in_range_context = context["last_page_is_in_range"]
        has_more_than_one_page_context = context["has_more_than_one_page"]
        

        self.assertEqual(len(recipes_context), per_page)
        self.assertEqual(list_context, pagination_list)
        self.assertEqual(current_page_context, current_page)
        self.assertEqual(first_page_context, first_page)
        self.assertEqual(last_page_context, last_page)
        self.assertEqual(first_page_is_in_range_context, first_page_is_in_range)
        self.assertEqual(last_page_is_in_range_context, last_page_is_in_range)
        self.assertEqual(has_more_than_one_page_context, has_more_than_one_page)
        
        for recipe in recipes_context:
            self.assertIn(recipe.title, content)