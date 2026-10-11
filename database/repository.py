from database.models import Post, User


def get_user(username):
    return User.first(username=username)


def get_all_posts():
    return Post.all()


def get_post(post_id):
    return Post.find(post_id)


def create_post(title, body):
    post = Post.create(title=title, body=body)
    return post.id