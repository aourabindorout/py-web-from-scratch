from utils.form_parser import parse_form
from web.request import Request


def parse_request(raw_request):
    if "\r\n\r\n" in raw_request:
        header_text, body = raw_request.split("\r\n\r\n", 1)
    else:
        header_text, body = raw_request, ""

    lines = header_text.split("\r\n")

    parts = lines[0].split() if lines else []
    method = parts[0] if len(parts) > 0 else "GET"
    path = parts[1] if len(parts) > 1 else "/"
    version = parts[2] if len(parts) > 2 else "HTTP/1.1"

    headers = {}
    for line in lines[1:]:
        if ": " in line:
            key, value = line.split(": ", 1)
            headers[key] = value

    form = {}
    if headers.get("Content-Type") == "application/x-www-form-urlencoded":
        form = parse_form(body)

    return Request(
        method=method,
        path=path,
        version=version,
        headers=headers,
        body=body,
        form=form
    )