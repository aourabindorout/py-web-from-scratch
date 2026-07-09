class Request:

    def __init__(
        self,
        method,
        path,
        version,
        headers,
        body,
        form
    ):
        self.method = method
        self.path = path
        self.version = version
        self.headers = headers
        self.body = body
        self.form = form or {}