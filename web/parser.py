from utils.form_parser import parse_form
from utils.query_parser import parse_query
from web.request import Request


def parse_request(raw_request):
    if "\r\n\r\n" in raw_request:
        header_text, body = raw_request.split("\r\n\r\n", 1)
    else:
        header_text, body = raw_request, ""

    lines = header_text.split("\r\n")

    parts = lines[0].split() if lines else []
    method = parts[0] if len(parts) > 0 else "GET"
    raw_target = parts[1] if len(parts) > 1 else "/"
    version = parts[2] if len(parts) > 2 else "HTTP/1.1"

    if "?" in raw_target:
        path, query_string = raw_target.split("?", 1)
    else:
        path, query_string = raw_target, ""

    query = parse_query(query_string)

    headers = {}
    for line in lines[1:]:
        if ": " in line:
            key, value = line.split(": ", 1)
            headers[key] = value

    form = {}
    content_type = ""
    cookie_header = ""
    for k, v in headers.items():
        k_lower = k.lower()
        if k_lower == "content-type":
            content_type = v
        elif k_lower == "cookie":
            cookie_header = v

    if content_type.startswith("application/x-www-form-urlencoded"):
        form = parse_form(body)

    cookies = {}
    if cookie_header:
        for part in cookie_header.split(";"):
            if "=" in part:
                c_key, c_val = part.split("=", 1)
                cookies[c_key.strip()] = c_val.strip()

    return Request(
        method=method,
        path=path,
        version=version,
        headers=headers,
        body=body,
        form=form,
        query=query,
        cookies=cookies
    )