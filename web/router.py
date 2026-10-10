import mimetypes
import os

from web.response import Response


class Router:

    def __init__(self, static_dir="static", static_prefix="/static"):
        self.routes = []
        if not os.path.isabs(static_dir):
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.static_dir = os.path.join(base_dir, static_dir)
        else:
            self.static_dir = os.path.abspath(static_dir)
        self.static_prefix = static_prefix.rstrip("/")

    def add_route(self, method, path, handler):
        self.routes.append((method, path, handler))

    def _serve_static(self, request_path):
        rel_path = request_path[len(self.static_prefix):].lstrip("/")
        file_path = os.path.abspath(os.path.join(self.static_dir, rel_path))

        # Security: Prevent directory traversal outside static_dir
        if not file_path.startswith(self.static_dir + os.sep) or not os.path.isfile(file_path):
            return Response(
                body="404 Not Found",
                status_code=404,
                reason="Not Found",
                headers={
                    "Content-Type": "text/plain"
                }
            )

        content_type, _ = mimetypes.guess_type(file_path)
        content_type = content_type or "application/octet-stream"

        with open(file_path, "rb") as f:
            content = f.read()

        return Response(
            body=content,
            status_code=200,
            reason="OK",
            headers={
                "Content-Type": content_type
            }
        )

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
        if request.method == "GET" and request.path.startswith(self.static_prefix + "/"):
            return self._serve_static(request.path)

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