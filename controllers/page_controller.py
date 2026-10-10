from database.repository import get_all_posts, get_post
from utils.render import render
from web.response import Response


def home(request):
    return render("home.html")


def posts(request):
    posts = get_all_posts()
    html = "".join(
        f'<li><a href="/posts/{post["id"]}">{post["title"]}</a></li>'
        for post in posts
    )

    return render(
        "posts.html",
        {
            "posts": html
        }
    )


def show_post(request):
    post_id = request.params.get("id")
    post = get_post(post_id)

    if post is None:
        return Response(
            body="404 Post Not Found",
            status_code=404,
            reason="Not Found",
            headers={
                "Content-Type": "text/plain"
            }
        )

    return render(
        "post.html",
        {
            "title": post["title"],
            "body": post.get("body", "")
        }
    )


def show_login(request):
    return render("login.html")