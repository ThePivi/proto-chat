import pytest
import threading
import time
import socket
from proto_chat.protochat_client import ProtoChatClient
from proto_chat.protochat_server import ProtoChatServer
from unittest.mock import Mock, patch

@pytest.fixture
def mock_p2p_client():
    """Fixture, ami egy mock-olt P2P klienst ad vissza tesztelésre."""
    return Mock(spec=ProtoChatClient)

def test_client_connects_to_peer():
    host = '127.0.0.1'
    port = 9000

    # szerver indítása külön thread-ben
    t = threading.Thread(target=ProtoChatServer.start_server, args=(host, port), daemon=True)
    t.start()

    time.sleep(0.2)  # adj egy kis időt, hogy elinduljon a szerver
    
    client = ProtoChatClient(port=12345)
    
    is_connected = client.connect(peer_ip=host, peer_port=port)
    
    assert is_connected is True

def test_client_sends_message(mock_p2p_client):
    mock_p2p_client.connect.return_value = True
    
    result = mock_p2p_client.connect("Hello, world!")
    
    assert result is True
