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

    return render(
        "posts.html",
        {
            "posts": all_posts,
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

    is_author = bool(request.user and str(post.get("user_id")) == str(request.user.id))

    return render(
        "post.html",
        {
            "post": post,
            "is_author": is_author
        },
        request=request
    )


@login_required
def new_post(request):
    return render("new_post.html", {"title": "", "body": "", "error": ""}, request=request)


@login_required
def create_new_post(request):
    title = request.form.get("title", "").strip()
    body = request.form.get("body", "").strip()

    if not title or not body:
        return render(
            "new_post.html",
            {
                "title": title,
                "body": body,
                "error": "Title and content cannot be empty."
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
            "post": post,
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
        temp_post = {"id": post.id, "title": title, "body": body}
        return render(
            "edit_post.html",
            {
                "post": temp_post,
                "error": "Title and content cannot be empty."
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
