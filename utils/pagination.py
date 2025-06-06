def pagination(
        num_total_pages: int,
        num_pages: int,  
        current_page: int,
        num_pages_before_current_page:int,
        num_pages_after_current_page: int
    ) -> dict:

    if num_pages_before_current_page + num_pages_after_current_page != (num_pages - 1):
        msg_error = "a soma da quantidade de páginas antes e depois da página atual \
         deve dar a quantidade de páginas a serem agrupadas menos um"
        raise ValueError(msg_error)
    
    if current_page < 1 or current_page > num_total_pages:
        msg_error = f"a página atual deve estar entre {1} e {num_total_pages}"
        raise ValueError(msg_error)
    
    first_page = 1
    last_page = num_total_pages
    pagination_list = []

    start_of_range = current_page - num_pages_before_current_page
    end_of_range = current_page + num_pages_after_current_page + 1
    middle_list = list(range(start_of_range, end_of_range))

    initial_list = list(range(first_page, num_pages + 1))
    final_list = list(range(last_page - num_pages + 1, last_page + 1))
    total_list = list(range(first_page, last_page + 1))

    if num_pages > num_total_pages:
        pagination_list =  total_list
    elif current_page - num_pages_before_current_page < first_page:
        pagination_list = initial_list
    elif current_page + num_pages_after_current_page > last_page:
        pagination_list = final_list
    else:
        pagination_list = middle_list

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