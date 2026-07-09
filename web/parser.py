from web.request import Request
from utils.form_parser import parse_form


def parse_request(raw_request):

    header_text, body = raw_request.split("\r\n\r\n", 1)

    lines = header_text.split("\r\n")

    method, path, version = lines[0].split()

    headers = {}

    for line in lines[1:]:
        key, value = line.split(": ", 1)
        headers[key] = value

    form = {}

    if headers.get("Content-Type") == "application/x-www-form-urlencoded":
        form = parse_form(body)

    return Request(
        method,
        path,
        version,
        headers,
        body,
        form
    )