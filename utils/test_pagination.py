from unittest import TestCase
from utils.pagination import pagination

class TestPagination(TestCase):

    def test_if_pagination_algorithm_returns_correct_pagination_when_num_pages_is_four(self):
        configuration_1 = {
            "num_total_pages": 20,
            "num_pages": 4,
            "num_pages_before_current_page": 1,
            "num_pages_after_current_page": 2
        }

        pagination1 = pagination(**configuration_1, current_page=10)
        pagination2 = pagination(**configuration_1, current_page=1)
        pagination3 = pagination(**configuration_1, current_page=19)
        
        self.assertEqual(pagination1["pagination_list"], [9, 10, 11, 12])
        self.assertEqual(pagination1["first_page_is_in_range"], False)
        self.assertEqual(pagination1["last_page_is_in_range"], False)


        self.assertEqual(pagination2["pagination_list"], [1, 2, 3, 4])
        self.assertEqual(pagination2["first_page_is_in_range"], True)
        self.assertEqual(pagination2["last_page_is_in_range"], False)

        self.assertEqual(pagination3["pagination_list"], [17, 18, 19, 20])
        self.assertEqual(pagination3["first_page_is_in_range"], False)
        self.assertEqual(pagination3["last_page_is_in_range"], True)
        
        