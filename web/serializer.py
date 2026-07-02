def serialize_response(response):

    lines = []

    # Status line
    lines.append(
        f"{response.version} {response.status_code} {response.reason}"
    )

    # Automatically add Content-Length if missing
    if "Content-Length" not in response.headers:
        response.headers["Content-Length"] = str(
            len(response.body.encode())
        )

    # Write headers
    for key, value in response.headers.items():
        lines.append(f"{key}: {value}")

    # Blank line between headers and body
    lines.append("")

    # Body
    lines.append(response.body)

    return "\r\n".join(lines)