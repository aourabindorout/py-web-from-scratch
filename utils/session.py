import secrets
from database.models import Session, User


def create_session(user_id):
    token = secrets.token_hex(32)
    Session.create(session_id=token, user_id=user_id)
    return token


def get_user_by_session_id(session_id):
    if not session_id:
        return None
    session = Session.first(session_id=session_id)
    if session:
        return User.find(session.user_id)
    return None


def delete_session(session_id):
    if not session_id:
        return
    session = Session.first(session_id=session_id)
    if session:
        session.delete()

