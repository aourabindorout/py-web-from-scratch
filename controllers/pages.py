from web.response import Response
from utils.template import load_template


def home(request):

    return Response(
        body=load_template("home.html"),
        headers={
            "Content-Type": "text/html"
        }
    )


def posts(request):

    return Response(
        body=load_template("posts.html"),
        headers={
            "Content-Type": "text/html"
        }
    )


def login(request):

    return Response(
        body=load_template("login.html"),
        headers={
            "Content-Type": "text/html"
        }
    )