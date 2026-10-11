from functools import wraps
from web.response import Response


def login_required(handler):
    @wraps(handler)
    def wrapper(request):
        if not getattr(request, "user", None):
            next_url = request.path
            return Response(
                status_code=302,
                reason="Found",
                headers={"Location": f"/login?next={next_url}"}
            )
        return handler(request)

    return wrapper

