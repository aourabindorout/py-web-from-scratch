from utils.render import render
from database.repository import get_all_posts
from web .response import Response

def home(request):
    return render("home.html")


def posts(request):

    posts = get_all_posts()

    html = ""

    for post in posts:
        html += f"<li>{post['title']}</li>"

    return render(
        "posts.html",
        {
            "posts": html
        }
    )


def login(request):

    username = request.form.get("username")

    return Response(
        body=f"Hello {username}",
        headers={
            "Content-Type": "text/plain"
        }
    )

def show_login(request):
    return render("login.html")