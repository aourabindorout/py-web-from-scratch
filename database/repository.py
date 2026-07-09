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
        "title": "Learning Python"
    },
    {
        "id": 2,
        "title": "Building My Own Web Framework"
    }
]


def get_user(username):
    return users.get(username)


def get_all_posts():
    return posts