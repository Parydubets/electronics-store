from store import create_app


def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing


def test_hello(client):
    response = client.get('/hello')
    assert response.data == b'Hello, World!'

def test_clients_route(client):
    response = client.get('/')
    assert response.status_code == 200
    response = client.get('/clients')
    assert response.status_code == 200
    #assert response.data.decode('utf-8') == 'Testing, Flask!'

def test_orders_route(client):
    response = client.get('/orders')
    assert response.status_code == 200

def test_products_route(client):
    response = client.get('/products')
    assert response.status_code == 200

def test_new_client_route(client):
    response = client.get('/new_client')
    assert response.status_code == 200

def test_new_order_route(client):
    response = client.get('/new_order')
    assert response.status_code == 200

def test_new_product_route(client):
    response = client.get('/new_product')
    assert response.status_code == 200
