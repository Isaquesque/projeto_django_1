from unittest import TestCase
from utils.pagination import pagination

class TestPagination(TestCase):

    def test_if_pagination_algorithm_returns_correct_pagination(self):
        configuration_1 = {
            "objects": range(1, 101),
            "num_pages": 4,
            "num_item_per_page": 5,
            "num_pages_before_current_page": 1,
            "num_pages_after_current_page": 2
        }
        
        self.assertEqual(pagination(**configuration_1, current_page=10), [9, 10, 11, 12])
        self.assertEqual(pagination(**configuration_1, current_page=1), [1, 2, 3, 4])
        self.assertEqual(pagination(**configuration_1, current_page=19), [17, 18, 19, 20])
        self.assertEqual(pagination(**configuration_1, current_page=20), [17, 18, 19, 20])
        