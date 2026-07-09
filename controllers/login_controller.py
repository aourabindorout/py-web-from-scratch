from database.repository import get_user
from web.response import Response


def login(request):

    username = request.form.get("username")
    password = request.form.get("password")

    user = get_user(username)

    if user is None:
        return Response(
            body="User not found",
            headers={
                "Content-Type": "text/plain"
            }
        )

    if user["password"] != password:
        return Response(
            body="Incorrect password",
            headers={
                "Content-Type": "text/plain"
            }
        )

    return Response(
        body=f"Welcome {username}",
        headers={
            "Content-Type": "text/plain"
        }
    )