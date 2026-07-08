import socket

from web.parser import parse_request
from web.response import Response
from web.serializer import serialize_response
from web.router import Router

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(("localhost", 8080))

server.listen()

print("Waiting...")

client, addr = server.accept()

raw_request = client.recv(4096).decode()

request = parse_request(raw_request)

print(request.method)
print(request.path)

def home(request):
    return Response(
        body="Welcome to the Home Page!",
        headers={
            "Content-Type": "text/plain"
        }
    )


def posts(request):
    return Response(
        body="All Blog Posts",
        headers={
            "Content-Type": "text/plain"
        }
    )


def login(request):
    return Response(
        body="Login Page",
        headers={
            "Content-Type": "text/plain"
        }
    )

router = Router()

router.add_route("GET", "/", home)
router.add_route("GET", "/posts", posts)
router.add_route("GET", "/login", login)

response = router.resolve(request)

raw_response = serialize_response(response)

client.send(raw_response.encode())

client.close()