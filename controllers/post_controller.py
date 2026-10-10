from database.repository import get_all_posts, get_post
from utils.render import render
from web.response import Response


def posts(request):
    all_posts = get_all_posts()
    search_query = request.query.get("search", "").strip()

    if search_query:
        all_posts = [
            post for post in all_posts
            if search_query.lower() in post["title"].lower()
            or search_query.lower() in post.get("body", "").lower()
        ]

    if all_posts:
        html = "".join(
            f'<li><a href="/posts/{post["id"]}">{post["title"]}</a></li>'
            for post in all_posts
        )
    else:
        html = "<p>No posts found matching your search.</p>"

    return render(
        "posts.html",
        {
            "posts": html,
            "search_query": search_query
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

