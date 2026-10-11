from database.models import Post
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
            f'<li><a href="/posts/{post.id}">{post.title}</a></li>'
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

    return render(
        "post.html",
        {
            "title": post.title,
            "body": post.get("body", "")
        },
        request=request
    )


def new_post(request):
    return render("new_post.html", {"error": ""}, request=request)


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


    Post.create(title=title, body=body)

    return Response(
        status_code=302,
        reason="Found",
        headers={
            "Location": "/posts"
        }
    )



