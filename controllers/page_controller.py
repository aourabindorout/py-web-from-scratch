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

    if all_posts:
        html = "".join(
            f'<li>'
            f'<a href="/posts/{post.id}">{post.title}</a>'
            f'<div class="post-meta" style="font-size: 0.85rem; color: var(--text-secondary); margin-top: 0.35rem;">'
            f'By {post.get("author_name") or "Community"}'
            f'</div>'
            f'</li>'
            for post in all_posts
        )
    else:
        html = "<p>No posts found matching your search.</p>"

    return render(
        "home.html",
        {
            "posts": html,
            "search_query": search_query
        },
        request=request
    )