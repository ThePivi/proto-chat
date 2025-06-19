# tests/test_app.py
from proto_chat.app import greet # Itt importáljuk az új package névről

def test_greet_function():
    assert greet("World") == "Hello, World!"
    assert greet("Jenkins") == "Hello, Jenkins!"
    assert greet("User") != "Goodbye, User!" # Egy negatív teszt