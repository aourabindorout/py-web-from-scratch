from database.models import User
from utils.render import render
from utils.session import create_session, delete_session
from web.response import Response


def show_login(request):
    if request.user:
        return Response(status_code=302, reason="Found", headers={"Location": "/"})
    return render("login.html", {"error": ""}, request=request)


def login(request):
    username = request.form.get("username", "")
    password = request.form.get("password", "")

    user = User.first(username=username)

    if user is None:
        return render(
            "login.html",
            {
                "error": '<div class="alert alert-error">User not found</div>'
            },
            request=request
        )

    if user.password != password:
        return render(
            "login.html",
            {
                "error": '<div class="alert alert-error">Incorrect password</div>'
            },
            request=request
        )

    # Authentication successful: create session & set cookie
    token = create_session(user.id)
    response = Response(
        status_code=302,
        reason="Found",
        headers={"Location": "/"}
    )
    response.set_cookie("session_id", token, path="/", http_only=True)
    return response


def logout(request):
    session_id = request.cookies.get("session_id")
    if session_id:
        delete_session(session_id)

    response = Response(
        status_code=302,
        reason="Found",
        headers={"Location": "/"}
    )
    response.delete_cookie("session_id", path="/")
    return response