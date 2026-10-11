from database.models import User
from utils.render import render
from utils.security import hash_password, verify_password
from utils.session import create_session, delete_session
from web.response import Response


def show_login(request):
    if request.user:
        return Response(status_code=302, reason="Found", headers={"Location": "/"})
    next_url = request.query.get("next", "")
    return render("login.html", {"error": "", "next": next_url}, request=request)


def login(request):
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")
    next_url = request.form.get("next") or request.query.get("next") or "/"

    user = User.first(username=username)

    if user is None:
        return render(
            "login.html",
            {
                "error": "User not found",
                "next": next_url
            },
            request=request
        )

    if not verify_password(password, user.password):
        return render(
            "login.html",
            {
                "error": "Incorrect password",
                "next": next_url
            },
            request=request
        )

    # Authentication successful: create session & set cookie
    token = create_session(user.id)
    target = next_url if next_url.startswith("/") else "/"
    response = Response(
        status_code=302,
        reason="Found",
        headers={"Location": target}
    )
    response.set_cookie("session_id", token, path="/", http_only=True)
    return response


def show_register(request):
    if request.user:
        return Response(status_code=302, reason="Found", headers={"Location": "/"})
    return render("register.html", {"error": "", "name": "", "username": ""}, request=request)


def register(request):
    name = request.form.get("name", "").strip()
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")
    confirm_password = request.form.get("confirm_password", "")

    if not name or not username or not password:
        return render(
            "register.html",
            {"error": "All fields are required.", "name": name, "username": username},
            request=request
        )

    if len(name) < 2:
        return render(
            "register.html",
            {"error": "Name must be at least 2 characters.", "name": name, "username": username},
            request=request
        )

    if len(username) < 3:
        return render(
            "register.html",
            {"error": "Username must be at least 3 characters.", "name": name, "username": username},
            request=request
        )

    if len(password) < 6:
        return render(
            "register.html",
            {"error": "Password must be at least 6 characters.", "name": name, "username": username},
            request=request
        )

    if password != confirm_password:
        return render(
            "register.html",
            {"error": "Passwords do not match.", "name": name, "username": username},
            request=request
        )

    # Check if username is already taken
    existing = User.first(username=username)
    if existing:
        return render(
            "register.html",
            {"error": "Username is already taken.", "name": name, "username": username},
            request=request
        )

    # Hash password with PBKDF2 + salt and create user
    hashed_password = hash_password(password)
    user = User.create(name=name, username=username, password=hashed_password)

    # Automatically log the user in with a new session
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