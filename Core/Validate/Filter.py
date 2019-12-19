import datetime


def arr_of_filters(str_type, log) -> dict:
    arr_of_filters = {}
    if str_type != 'date':
        arr_of_filters = {
            '=': lambda x, y: x == y,
            '>': lambda x, y: x > int(y),
            '>=': lambda x, y: x >= int(y),
            '<': lambda x, y: x < int(y),
            '<=': lambda x, y: x <= int(y),
            '!=': lambda x, y: x != y
        }
    elif str_type == 'date':
        arr_of_filters = {
            '=': lambda x, y: datetime.datetime.strptime(str(x), "%Y%m%d") == datetime.datetime.strptime(str(y), "%Y.%m.%d"),
            '>': lambda x, y: datetime.datetime.strptime(str(x), "%Y%m%d") > datetime.datetime.strptime(str(y), "%Y.%m.%d"),
            '>=': lambda x, y: datetime.datetime.strptime(str(x), "%Y%m%d") >= datetime.datetime.strptime(str(y), "%Y.%m.%d"),
            '<': lambda x, y: datetime.datetime.strptime(str(x), "%Y%m%d") < datetime.datetime.strptime(str(y), "%Y.%m.%d"),
            '<=': lambda x, y: datetime.datetime.strptime(str(x), "%Y%m%d") <= datetime.datetime.strptime(str(y), "%Y.%m.%d"),
            '!=': lambda x, y: datetime.datetime.strptime(str(x), "%Y%m%d") != datetime.datetime.strptime(str(y), "%Y.%m.%d")
        }
    else:
        log.raiseInfo(44, f'Unknown data type of the column <{str_type}>')

    return arr_of_filters

def filter_vals(log, str_type, mode, filter_value, value):
    return arr_of_filters(str_type, log)[mode](value, filter_value)

def filter_arr(log, str_type, arr, value):
    flag = False
    for i in arr:
        flag = filter_vals(log, str_type, i["filterMode"], i["filterValue"], value) or flag
    if flag:
        return True
    return False
