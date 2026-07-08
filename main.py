import socket

from web.parser import parse_request
from web.response import Response
from web.serializer import serialize_response
from web.router import Router
from controllers.page_controller import (home,posts,login)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(("localhost", 8080))

server.listen()

router = Router()
router.add_route("GET", "/", home)
router.add_route("GET", "/posts", posts)
router.add_route("GET", "/login", login)

print("Server started on http://localhost:8080")

while True:

    client, addr = server.accept()

    raw_request = client.recv(4096).decode()

    request = parse_request(raw_request)

    response = router.resolve(request)

    raw_response = serialize_response(response)

    client.send(raw_response.encode())

    client.close()