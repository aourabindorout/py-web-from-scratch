from database.repository import get_user
from utils.render import render


def show_login(request):
    return render("login.html", {"error": ""})


def login(request):
    username = request.form.get("username", "")
    password = request.form.get("password", "")

    user = get_user(username)

    if user is None:
        return render(
            "login.html",
            {
                "error": '<div class="alert alert-error">User not found</div>'
            }
        )

    if user["password"] != password:
        return render(
            "login.html",
            {
                "error": '<div class="alert alert-error">Incorrect password</div>'
            }
        )

    return render(
        "welcome.html",
        {
            "username": username
        }
    )