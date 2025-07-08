# src/proto_chat/protochat_server.py
import socket


class ProtoChatServer:
    def start_server(host, port):
        s = socket.socket()
        s.bind((host, port))
        s.listen(1)
        conn, _ = s.accept()
        data = conn.recv(1024)
        if data:
            conn.sendall(b'ACK')
        conn.close()
        s.close()

    def create_socket():
        return socket.socket()

    def bind_socket(sock, host, port):
        sock.bind((host, port))

    def start_listening(sock):
        sock.listen(1)

    def accept_connection(sock):
        conn, addr = sock.accept()
        return conn, addr

    def handle_client(conn):
        data = conn.recv(1024)
        if data == b'ping':
            conn.sendall(b'pong')
        else:
            conn.sendall(b'error')
        conn.close()