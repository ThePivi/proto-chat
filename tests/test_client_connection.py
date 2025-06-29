# tests/test_client_connection.py
import pytest
from your_module_name.client import P2PClient

# Cél: Tesztelni a connect metódust
def test_client_connects_to_peer():
    """
    Teszt: Ellenőrzi, hogy a kliens sikeresen tud-e csatlakozni egy peerhez.
    """
    # Arrange
    # Itt mock-oljuk a hálózati kommunikációt, hogy ne kelljen valódi szervert futtatni.
    # Ez a "unit test", ami az adott egységet (itt a 'connect' metódust) teszteli izoláltan.
    mock_socket = Mock() # A 'mock' könyvtárból
    client = P2PClient(port=12345)
    
    # Act
    # Hívjuk a connect metódust
    is_connected = client.connect(peer_ip="127.0.0.1", peer_port=54321)
    
    # Assert
    # Ellenőrizzük, hogy a metódus 'True'-val tért vissza, jelezve a sikert.
    assert is_connected is True