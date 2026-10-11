from database.models import Post
from utils.render import render


def home(request):
    all_posts = Post.all()
    search_query = request.query.get("search", "").strip()

    if search_query:
        all_posts = [
            post for post in all_posts
            if search_query.lower() in post.title.lower()
            or search_query.lower() in post.get("body", "").lower()
        ]

    return render(
        "home.html",
        {
            "posts": all_posts,
            "search_query": search_query
        },
        request=request
    )