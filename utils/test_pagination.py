from unittest import TestCase
from utils.pagination import pagination

class TestPagination(TestCase):
    def setUp(self):
        self.configuration = {
            "num_total_pages": 20,
            "num_pages": 4,
            "num_pages_before_current_page": 1,
            "num_pages_after_current_page": 2
        }

    def test_middle_range(self):
        result = pagination(**self.configuration, current_page=10)
        self.assertEqual(result["pagination_list"], [9,10,11,12])

    def test_start_range(self):
        result = pagination(**self.configuration, current_page=1)
        self.assertEqual(result["pagination_list"], [1,2,3,4])

    def test_end_range(self):
        result = pagination(**self.configuration, current_page=19)
        self.assertEqual(result["pagination_list"], [17,18,19,20])

    def test_show_all_when_num_pages_exceeds_num_total_pages(self):
        self.configuration["num_total_pages"] = 3
        result = pagination(**self.configuration, current_page=3)
        self.assertEqual(result["pagination_list"], [1,2,3])

    def test_invalid_num_before_and_num_after_raises_error(self):
        self.configuration["num_pages_before_current_page"] = 2
        self.configuration["num_pages_after_current_page"] = 2

        raised_error = False
        try:
            result = pagination(**self.configuration, current_page=3)
        except ValueError:
            raised_error = True
        finally:
                self.assertTrue(raised_error)

    def test_invalid_current_page_raises_error(self):
        raised_error = False
        try:
            pagination(**self.configuration, current_page=21)
        except ValueError:
            raised_error = True
        finally:
                self.assertTrue(raised_error)

    def test_single_page(self):
        self.configuration["num_pages"] = 1
        self.configuration["num_pages_before_current_page"] = 0
        self.configuration["num_pages_after_current_page"] = 0

        result = pagination(**self.configuration, current_page=15)
        self.assertEqual(result["pagination_list"],[15])

    def test_flags(self):
        result = pagination(**self.configuration, current_page=19)

        self.assertFalse(result["first_page_is_in_range"])
        self.assertTrue(result["last_page_is_in_range"])
        self.assertTrue(result["has_more_than_one_page"])
        