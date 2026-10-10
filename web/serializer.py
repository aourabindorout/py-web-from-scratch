def serialize_response(response):
    body_bytes = (
        response.body.encode("utf-8")
        if isinstance(response.body, str)
        else response.body
    )

    if "Content-Length" not in response.headers:
        response.headers["Content-Length"] = str(len(body_bytes))

    header_lines = [
        f"{response.version} {response.status_code} {response.reason}"
    ]
    for key, value in response.headers.items():
        header_lines.append(f"{key}: {value}")

    header_bytes = ("\r\n".join(header_lines) + "\r\n\r\n").encode("utf-8")

    return header_bytes + body_bytes