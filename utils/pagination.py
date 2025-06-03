
def pagination(
        objects, 
        num_pages: int, 
        num_item_per_page: int, 
        current_page: int,
        num_pages_before_current_page:int,
        num_pages_after_current_page: int
    ):
    if num_pages_before_current_page + num_pages_after_current_page != (num_pages - 1):
        return
    
    num_total_pages = len(objects) // num_item_per_page if len(objects) % num_item_per_page == 0 else (len(objects) // num_item_per_page) + 1
    
    first_page = 1
    last_page = num_total_pages

    if current_page - num_pages_before_current_page <= first_page:
        return list(range(first_page, num_pages + 1))
    elif current_page + num_pages_after_current_page > last_page:
        return list(range(last_page - num_pages + 1, last_page + 1))
    else:
        return list(range(current_page - num_pages_before_current_page, current_page + num_pages_after_current_page + 1))

print(pagination(
    range(1,101),
    5,
    6,
    10,
    2,
    2
    )
)