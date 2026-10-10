def parse_form(body):
    data = {}
    if not body:
        return data

    for pair in body.split("&"):
        if "=" in pair:
            key, value = pair.split("=", 1)
            data[key] = value

    return data