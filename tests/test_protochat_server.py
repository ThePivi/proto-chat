# tests/test_protochat_server.py
import pytest
import socket
import threading
import time
from proto_chat.protochat_server import ProtoChatServer
from unittest.mock import Mock

def test_bind_socket_calls_bind_correctly():
    mock_sock = Mock()
    ProtoChatServer.bind_socket(mock_sock, 'localhost', 1234)
    mock_sock.bind.assert_called_once_with(('localhost', 1234))

def test_handle_client_sends_pong():
    mock_conn = Mock()
    mock_conn.recv.return_value = b'ping'

    ProtoChatServer.handle_client(mock_conn)

    mock_conn.sendall.assert_called_once_with(b'pong')
    mock_conn.close.assert_called_once()

def test_server_accepts_connection():
    host = '127.0.0.1'
    port = 9001

    # szerver indítása külön thread-ben
    t = threading.Thread(target=ProtoChatServer.start_server, args=(host, port), daemon=True)
    t.start()

    time.sleep(0.2)  # adj egy kis időt, hogy elinduljon a szerver

    # próbáljunk csatlakozni
    client_socket = socket.socket()
    client_socket.connect((host, port))
    client_socket.sendall(b'Hello')
    data = client_socket.recv(1024)
    client_socket.close()

    assert data == b'ACK'  # elvárjuk, hogy a szerver ACK-ot küld vissza