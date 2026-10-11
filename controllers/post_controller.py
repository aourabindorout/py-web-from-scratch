from database.models import Post
from utils.auth import login_required
from utils.render import render
from web.response import Response


def posts(request):
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
        "posts.html",
        {
            "posts": html,
            "search_query": search_query
        },
        request=request
    )


def show_post(request):
    post_id = request.params.get("id")
    post = Post.find(post_id)

    if post is None:
        return Response(
            body="404 Post Not Found",
            status_code=404,
            reason="Not Found",
            headers={
                "Content-Type": "text/plain"
            }
        )

    is_author = request.user and str(post.get("user_id")) == str(request.user.id)
    if is_author:
        author_actions = (
            f'<div style="display: flex; gap: 0.75rem; margin-top: 1.5rem;">'
            f'<a href="/posts/{post.id}/edit" class="btn">Edit Post</a>'
            f'<form action="/posts/{post.id}/delete" method="POST" style="margin: 0;" onsubmit="return confirm(\'Are you sure you want to delete this post?\');">'
            f'<button type="submit" class="btn" style="background: #ef4444; border-color: #dc2626; color: #fff;">Delete Post</button>'
            f'</form>'
            f'</div>'
        )
    else:
        author_actions = ""

    return render(
        "post.html",
        {
            "title": post.title,
            "body": post.get("body", ""),
            "author": post.get("author_name") or "Community",
            "author_actions": author_actions
        },
        request=request
    )


@login_required
def new_post(request):
    return render("new_post.html", {"error": ""}, request=request)


@login_required
def create_new_post(request):
    title = request.form.get("title", "").strip()
    body = request.form.get("body", "").strip()

    if not title or not body:
        return render(
            "new_post.html",
            {
                "error": '<div class="alert alert-error">Title and content cannot be empty.</div>'
            },
            request=request
        )

    author_name = getattr(request.user, "name", None) or request.user.username
    Post.create(
        title=title,
        body=body,
        user_id=request.user.id,
        author_name=author_name
    )

    return Response(
        status_code=302,
        reason="Found",
        headers={
            "Location": "/"
        }
    )


@login_required
def edit_post(request):
    post_id = request.params.get("id")
    post = Post.find(post_id)

    if post is None:
        return Response(
            body="404 Post Not Found",
            status_code=404,
            reason="Not Found",
            headers={"Content-Type": "text/plain"}
        )

    if str(post.get("user_id")) != str(request.user.id):
        return Response(
            body="403 Forbidden: You can only edit your own posts.",
            status_code=403,
            reason="Forbidden",
            headers={"Content-Type": "text/plain"}
        )

    return render(
        "edit_post.html",
        {
            "id": post.id,
            "title": post.title,
            "body": post.get("body", ""),
            "error": ""
        },
        request=request
    )


@login_required
def update_post(request):
    post_id = request.params.get("id")
    post = Post.find(post_id)

    if post is None:
        return Response(
            body="404 Post Not Found",
            status_code=404,
            reason="Not Found",
            headers={"Content-Type": "text/plain"}
        )

    if str(post.get("user_id")) != str(request.user.id):
        return Response(
            body="403 Forbidden: You can only edit your own posts.",
            status_code=403,
            reason="Forbidden",
            headers={"Content-Type": "text/plain"}
        )

    title = request.form.get("title", "").strip()
    body = request.form.get("body", "").strip()

    if not title or not body:
        return render(
            "edit_post.html",
            {
                "id": post.id,
                "title": title,
                "body": body,
                "error": '<div class="alert alert-error">Title and content cannot be empty.</div>'
            },
            request=request
        )

    post.update(title=title, body=body)

    return Response(
        status_code=302,
        reason="Found",
        headers={"Location": f"/posts/{post.id}"}
    )


@login_required
def delete_post(request):
    post_id = request.params.get("id")
    post = Post.find(post_id)

    if post is None:
        return Response(
            body="404 Post Not Found",
            status_code=404,
            reason="Not Found",
            headers={"Content-Type": "text/plain"}
        )

    if str(post.get("user_id")) != str(request.user.id):
        return Response(
            body="403 Forbidden: You can only delete your own posts.",
            status_code=403,
            reason="Forbidden",
            headers={"Content-Type": "text/plain"}
        )

    post.delete()

    return Response(
        status_code=302,
        reason="Found",
        headers={"Location": "/"}
    )

