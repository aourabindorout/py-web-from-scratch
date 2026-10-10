from urllib.parse import unquote_plus


def parse_form(body):
    data = {}
    if not body:
        return data

    for pair in body.split("&"):
        if "=" in pair:
            key, value = pair.split("=", 1)
            data[unquote_plus(key)] = unquote_plus(value)

    return data