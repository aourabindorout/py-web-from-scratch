from utils.render import render


def home(request):
    return render("home.html")


def posts(request):
    return render("posts.html")


def login(request):
    return render("login.html")