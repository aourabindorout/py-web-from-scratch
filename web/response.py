class Response:

    def __init__(self, body="", status_code=200, reason="OK", headers=None, version="HTTP/1.1"):
        self.version = version
        self.status_code = status_code
        self.reason = reason
        self.body = body
        self.headers = headers or {}