from database.repository import get_user
from web import Response


def login(request):

    username = request.form["username"]
    password = request.form["password"]

    user = get_user(username)

    if user is None:
        return Response(body="User not found")

    if user["password"] != password:
        return Response(body="Wrong password")

    return Response(body="Login Successful")