def pagination(
        num_total_pages: int,
        num_pages: int,  
        current_page: int,
        num_pages_before_current_page:int,
        num_pages_after_current_page: int
    ):

    if num_pages_before_current_page + num_pages_after_current_page != (num_pages - 1):
        return
    
    first_page = 1
    last_page = num_total_pages
    pagination_list = []

    if num_pages > num_total_pages:
        pagination_list =  list(range(1, num_total_pages+1))
    elif current_page - num_pages_before_current_page <= first_page:
        pagination_list = list(range(first_page, num_pages + 1))
    elif current_page + num_pages_after_current_page > last_page:
        pagination_list = list(range(num_total_pages - num_pages + 1, num_total_pages + 1))
    else:
        pagination_list = list(range(current_page - num_pages_before_current_page, current_page + num_pages_after_current_page + 1))

    return {
        "pagination_list": pagination_list,
        "current_page":current_page,
        "first_page":first_page,
        "last_page":last_page,
        "first_page_is_in_range": first_page in pagination_list,
        "last_page_is_in_range": last_page in pagination_list,
        "has_more_than_one_page": len(pagination_list) > 1
    }

if __name__ == "__main__":
    print(pagination(
        100,
        4,
        19,
        1,
        2
        )
    )