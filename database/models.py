from database.model import Model


class User(Model):
    table_name = "users"

    @property
    def display_name(self):
        return self.get("name") or self.username


class Post(Model):
    table_name = "posts"


class Session(Model):
    table_name = "sessions"
