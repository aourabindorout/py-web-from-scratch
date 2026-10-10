users = {
    "admin": {
        "password": "admin123"
    },
    "john": {
        "password": "john123"
    }
}


posts = [
    {
        "id": 1,
        "title": "Learning Python",
        "body": "Python is a versatile programming language with a clean, readable syntax."
    },
    {
        "id": 2,
        "title": "Building My Own Web Framework",
        "body": "Building web frameworks from scratch helps you understand sockets, HTTP protocols, and routing."
    }
]


def get_user(username):
    return users.get(username)


def get_all_posts():
    return posts


def get_post(post_id):
    for post in posts:
        if str(post["id"]) == str(post_id):
            return post
    return None