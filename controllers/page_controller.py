from database.repository import get_all_posts
from utils.render import render


def home(request):
    return render("home.html")


def posts(request):
    posts = get_all_posts()
    html = "".join(f"<li>{post['title']}</li>" for post in posts)

    return render(
        "posts.html",
        {
            "posts": html
        }
    )


def show_login(request):
    return render("login.html")