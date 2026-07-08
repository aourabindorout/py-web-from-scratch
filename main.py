import socket

from web.parser import parse_request
from web.response import Response
from web.serializer import serialize_response
from web.router import Router
from controllers.pages import (home,posts,login)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(("localhost", 8080))

server.listen()

print("Waiting...")

client, addr = server.accept()

raw_request = client.recv(4096).decode()

request = parse_request(raw_request)

print(request.method)
print(request.path)

router = Router()
router.add_route("GET", "/", home)
router.add_route("GET", "/posts", posts)
router.add_route("GET", "/login", login)

response = router.resolve(request)

raw_response = serialize_response(response)

client.send(raw_response.encode())

client.close()