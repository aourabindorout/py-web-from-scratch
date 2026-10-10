import socket

from controllers.login_controller import login
from controllers.page_controller import home, posts, show_login, show_post
from web.parser import parse_request
from web.router import Router
from web.serializer import serialize_response

router = Router()
router.add_route("GET", "/", home)
router.add_route("GET", "/posts", posts)
router.add_route("GET", "/posts/{id}", show_post)
router.add_route("GET", "/login", show_login)
router.add_route("POST", "/login", login)


def run_server(host="localhost", port=8080):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen()

    print(f"Server started on http://{host}:{port}")

    while True:
        client, addr = server.accept()
        raw_request = client.recv(4096).decode()

        if not raw_request:
            client.close()
            continue

        request = parse_request(raw_request)
        print(f"{request.method} {request.path}")

        response = router.resolve(request)
        raw_response = serialize_response(response)

        client.send(raw_response.encode())
        client.close()


if __name__ == "__main__":
    run_server()
