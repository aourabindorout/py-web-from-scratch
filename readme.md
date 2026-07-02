# Py Web From Scratch

A learning project to understand how modern Python web frameworks work by building one from first principles.

The objective is **not** to use frameworks like Django or Flask, but to understand the abstractions they provide by implementing them ourselves in pure Python.

The project begins with raw TCP sockets and gradually builds higher-level web framework components, using a simple blog application as the driving example.

## Why this project?

Web frameworks hide a tremendous amount of complexity behind simple APIs.

For example:

```python
@app.route("/posts")
def show_posts():
    ...
```

Behind this seemingly simple code, a framework has already:

* Accepted a TCP connection
* Received bytes from the network
* Parsed an HTTP request
* Constructed a request object
* Routed the request to the correct handler
* Built an HTTP response
* Serialized that response back into bytes
* Sent it back to the client

The purpose of this project is to understand each of these layers by implementing them ourselves.

## Learning Goals

* Understand TCP sockets
* Build a simple HTTP server
* Parse HTTP requests
* Construct HTTP responses
* Implement request routing
* Build controllers and middleware
* Add template rendering
* Implement sessions and cookies
* Implement authentication and authorization
* Integrate a database
* Build a complete blog application without using an existing web framework

## Current Progress

* ✅ TCP socket server
* ✅ Browser-to-server communication
* ✅ HTTP request parsing
* ✅ Request object abstraction
* ✅ HTTP response generation
* ✅ Response serialization

## Planned Roadmap

* Request routing
* Dynamic route parameters
* Query parameter parsing
* HTML responses
* Template engine
* Static file serving
* Forms and POST requests
* SQLite integration
* ORM (minimal)
* Session management
* Authentication
* Authorization
* JWT authentication
* Production-ready project structure

## Repository Structure

```text
blog/
│
├── main.py
│
├── web/
│   ├── parser.py
│   ├── request.py
│   ├── response.py
│   └── serializer.py
│
└── utils/
```

## Philosophy

This repository is intentionally built without Django, Flask, FastAPI, or other web frameworks.

The emphasis is on understanding the layers that sit beneath those frameworks rather than relying on them.

The goal is not to build the fastest or most feature-rich framework, but to gain a solid understanding of how web applications work internally.

## Inspiration

The best way to understand an abstraction is to build a simpler version of it.

This repository is an exploration of the engineering behind modern Python web frameworks, one layer at a time.
