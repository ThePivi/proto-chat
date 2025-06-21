from proto_chat.app import greet


def test_greet_function():
    assert greet("World") == "Hello, World!"
    assert greet("Jenkins") == "Hello, Jenkins!"
    assert greet("User") == "Hello, User!"
    assert greet("User") != "Goodbye, User!"
