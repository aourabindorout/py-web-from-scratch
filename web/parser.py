from web.request import Request


def parse_request(raw_request):
    lines = raw_request.split("\r\n")

    request_line = lines[0]

    method, path, version = request_line.split()

    headers = {}

    for line in lines[1:]:
        if line == "":
            break

        key, value = line.split(": ", 1)
        headers[key] = value

    body = ""

    return Request(method, path, version, headers, body)