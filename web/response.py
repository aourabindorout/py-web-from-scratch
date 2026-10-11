class Response:

    def __init__(self, body="", status_code=200, reason="OK", headers=None, version="HTTP/1.1"):
        self.version = version
        self.status_code = status_code
        self.reason = reason
        self.body = body
        self.headers = headers or {}
        self.cookies = {}

    def set_cookie(self, name, value, path="/", http_only=True, max_age=None):
        parts = [f"{name}={value}", f"Path={path}"]
        if http_only:
            parts.append("HttpOnly")
        if max_age is not None:
            parts.append(f"Max-Age={max_age}")
        self.cookies[name] = "; ".join(parts)

    def delete_cookie(self, name, path="/"):
        self.set_cookie(name, "", path=path, max_age=0)