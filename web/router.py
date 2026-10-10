from web.response import Response


class Router:

    def __init__(self):
        self.routes = []

    def add_route(self, method, path, handler):
        self.routes.append((method, path, handler))

    def _match_path(self, route_path, request_path):
        route_segments = [s for s in route_path.strip("/").split("/") if s]
        req_segments = [s for s in request_path.strip("/").split("/") if s]

        if len(route_segments) != len(req_segments):
            return False, {}

        params = {}
        for r_seg, q_seg in zip(route_segments, req_segments):
            if r_seg.startswith("{") and r_seg.endswith("}"):
                param_name = r_seg[1:-1]
                params[param_name] = q_seg
            elif r_seg != q_seg:
                return False, {}

        return True, params

    def resolve(self, request):
        for method, path, handler in self.routes:
            if method != request.method:
                continue

            matched, params = self._match_path(path, request.path)
            if matched:
                request.params = params
                return handler(request)

        return Response(
            body="404 Not Found",
            status_code=404,
            reason="Not Found",
            headers={
                "Content-Type": "text/plain"
            }
        )