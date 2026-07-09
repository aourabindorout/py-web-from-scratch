from utils.render import render
from database.repository import get_all_posts

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
    return render("login.html")

def show_login(request):
    return render("login.html")