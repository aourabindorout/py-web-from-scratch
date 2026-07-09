def parse_form(body):

    data = {}

    if body == "":
        return data

    pairs = body.split("&")

    for pair in pairs:

        key, value = pair.split("=", 1)

        data[key] = value

    return data