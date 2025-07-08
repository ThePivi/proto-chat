# src/proto_chat/protochat_client.py
import socket


class ProtoChatClient:
    def __init__(self, port):
        self.port = port
        self.connected_peers = []
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, peer_ip, peer_port):
        try:
            self.socket.connect((peer_ip, peer_port))
            # Itt lenne a valós csatlakozási logika
            # Ha sikeres, hozzáadjuk a peert a listához
            self.connected_peers.append((peer_ip, peer_port))
            return True
        except socket.error:
            # Ha hiba van a csatlakozásnál
            return False

    def sendall(self, msg):
        self.socket.sendall(msg.encode('utf-8'))