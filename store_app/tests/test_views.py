from store import create_app


def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing


def test_hello(client):
    response = client.get('/hello')
    assert response.data == b'Hello, World!'

def test_clients(client):
    response = client.get("/clients")
    assert response.request.path == "/clients"
    assert response.status_code ==200