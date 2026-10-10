class Request:

    def __init__(
        self,
        method,
        path,
        version="HTTP/1.1",
        headers=None,
        body="",
        form=None,
        params=None
    ):
        self.method = method
        self.path = path
        self.version = version
        self.headers = headers or {}
        self.body = body
        self.form = form or {}
        self.params = params or {}