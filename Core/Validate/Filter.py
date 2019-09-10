arr_of_filters = {
    '=': lambda x, y: x == y,
    '>': lambda x, y: x > int(y),
    '>=': lambda x, y: x >= int(y),
    '<': lambda x, y: x < int(y),
    '<=': lambda x, y: x <= int(y),
    '!=': lambda x, y: x != y
}

def filter_vals(mode, filter_value, value):
    return arr_of_filters[mode](value, filter_value)

def filter_arr(arr, value):
    flag = False
    for i in arr:
        flag = filter_vals(i["filterMode"], i["filterValue"], value) or flag
    if flag:
        return True
    return False
