from urllib.parse import unquote_plus


def parse_query(query_string):
    data = {}
    if not query_string:
        return data

    for pair in query_string.split("&"):
        if "=" in pair:
            key, value = pair.split("=", 1)
            data[unquote_plus(key)] = unquote_plus(value)
        elif pair:
            data[unquote_plus(pair)] = ""

    return data

