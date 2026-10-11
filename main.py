import os
import socket
import traceback

from controllers.login_controller import login, logout, register, show_login, show_register
from controllers.page_controller import home
from controllers.post_controller import (
    create_new_post,
    delete_post,
    edit_post,
    new_post,
    posts,
    show_post,
    update_post,
)
from database.db import init_db
from utils.session import get_user_by_session_id
from web.parser import parse_request
from web.response import Response
from web.router import Router
from web.serializer import serialize_response

router = Router()
router.add_route("GET", "/", home)
router.add_route("GET", "/posts", posts)
router.add_route("GET", "/posts/new", new_post)
router.add_route("POST", "/posts/new", create_new_post)
router.add_route("GET", "/posts/{id}/edit", edit_post)
router.add_route("POST", "/posts/{id}/edit", update_post)
router.add_route("POST", "/posts/{id}/delete", delete_post)
router.add_route("GET", "/posts/{id}", show_post)
router.add_route("GET", "/login", show_login)
router.add_route("POST", "/login", login)
router.add_route("GET", "/register", show_register)
router.add_route("POST", "/register", register)
router.add_route("GET", "/logout", logout)






def receive_request(client):
    client.settimeout(5.0)
    buffer = bytearray()

    try:
        while b"\r\n\r\n" not in buffer:
            chunk = client.recv(4096)
            if not chunk:
                break
            buffer.extend(chunk)

        if not buffer:
            return ""

        header_bytes, sep, body_bytes = buffer.partition(b"\r\n\r\n")
        if not sep:
            return header_bytes.decode("utf-8", errors="replace")

        # Parse Content-Length to receive the full body if larger than initial buffer
        content_length = 0
        header_text = header_bytes.decode("utf-8", errors="replace")
        for line in header_text.split("\r\n"):
            if ":" in line:
                key, val = line.split(":", 1)
                if key.strip().lower() == "content-length":
                    try:
                        content_length = int(val.strip())
                    except ValueError:
                        content_length = 0
                    break

        while len(body_bytes) < content_length:
            remaining = content_length - len(body_bytes)
            chunk = client.recv(min(4096, remaining))
            if not chunk:
                break
            body_bytes.extend(chunk)

        return (header_bytes + sep + body_bytes).decode("utf-8", errors="replace")
    except (socket.timeout, OSError):
        if buffer:
            return buffer.decode("utf-8", errors="replace")
        return ""


def run_server(host="localhost", port=8080):
    host = os.environ.get("HOST", host)
    port = int(os.environ.get("PORT", port))
    init_db()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen()

    print(f"Server started on http://{host}:{port}")

    while True:
        client, addr = server.accept()
        try:
            raw_request = receive_request(client)
            if not raw_request:
                continue

            request = parse_request(raw_request)
            session_id = request.cookies.get("session_id")
            request.user = get_user_by_session_id(session_id) if session_id else None
            user_label = f" [{request.user.username}]" if request.user else ""
            print(f"{request.method} {request.path}{user_label}")


            try:
                response = router.resolve(request)
            except Exception:
                traceback.print_exc()
                response = Response(
                    body="500 Internal Server Error",
                    status_code=500,
                    reason="Internal Server Error",
                    headers={"Content-Type": "text/plain"}
                )

            raw_response = serialize_response(response)
            client.sendall(raw_response)
        except (ConnectionResetError, BrokenPipeError):
            pass
        finally:
            client.close()


if __name__ == "__main__":
    run_server()
