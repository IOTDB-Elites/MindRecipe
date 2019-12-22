def get_one_json_item(items, filter):
    for cur_item in items:
        hasfound = True
        for field, value in filter.items():
            if cur_item[field] != value:
                hasfound = False
                break
        if hasfound:
            return cur_item
    return {}