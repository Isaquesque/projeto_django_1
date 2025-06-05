from utils.pagination import pagination
from django.core.paginator import Paginator

def make_pagination(
        request,
        objects,
        qty_items_per_page: int,
        num_pages: int,
        num_pages_before_current_page: int,
        num_pages_after_current_page: int
):
    try:
        current_page = int(request.GET.get("page", 1))
    except ValueError:
        current_page = 1
    
    paginator = Paginator(objects, qty_items_per_page)

    pagination_dict = pagination(
        paginator.num_pages,
        num_pages,
        current_page,
        num_pages_before_current_page,
        num_pages_after_current_page
    )

    pagination_dict = {
        "recipes": paginator.page(current_page).object_list,
        "pagination_list": pagination_dict["pagination_list"],
        "current_page": pagination_dict["current_page"],
        "first_page": pagination_dict["first_page"],
        "last_page": pagination_dict["last_page"],
        "first_page_is_in_range": pagination_dict["first_page_is_in_range"],
        "last_page_is_in_range": pagination_dict["last_page_is_in_range"],
        "has_more_than_one_page": pagination_dict["has_more_than_one_page"]
    }

    return pagination_dict