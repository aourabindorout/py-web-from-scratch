from web.response import Response


class Router:

    def __init__(self):
        self.routes = {}

    def add_route(self, method, path, handler):
        self.routes[(method, path)] = handler

    def resolve(self, request):

        handler = self.routes.get(
            (request.method, request.path)
        )

        if handler is None:
            return Response(
                body="404 Not Found",
                status_code=404,
                reason="Not Found",
                headers={
                    "Content-Type": "text/plain"
                }
            )

        return handler(request)