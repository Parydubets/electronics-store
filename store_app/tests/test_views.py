from flask  import request, url_for
from store import create_app
from store.views import *

def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing


"""def test_seed(client):
    print(create_app().seed())
    assert create_app().seed() == "Seeded successfully"""

def test_clients_route(client):
    response = client.get('/')
    assert response.status_code == 200
    response = client.get('/clients')
    assert response.status_code == 200
    #response = client.get('/clients', date_from='2023-01-01', date_to='2023-02-01')


    #assert response.data.decode('utf-8') == 'Testing, Flask!'

def test_new_client_route(client):
    response = client.get('/new_client')
    assert response.status_code == 200


def test_edit_client_route(client):
    response = client.get('/edit_client')
    assert response.status_code == 404
    response = client.get('/edit_client/1')
    assert response.status_code == 200
    response = client.get(('/edit_client/999'), follow_redirects=True)
    assert response.request.path == '/clients'

def test_orders_route(client):
    response = client.get('/orders')
    assert response.status_code == 200


def test_new_order_route(client):
    response = client.get('/new_client')
    assert response.status_code == 200


def test_edit_order_route(client):
    response = client.get('/edit_order')
    assert response.status_code == 404
    response = client.get('/edit_order/1')
    assert response.status_code == 200
    response = client.get(('/edit_order/999'), follow_redirects=True)
    assert response.request.path == '/orders'


def test_products_route(client):
    response = client.get('/products')
    assert response.status_code == 200


def test_new_product_route(client):
    response = client.get('/new_client')
    assert response.status_code == 200


def test_edit_product_route(client):
    response = client.get('/edit_client')
    assert response.status_code == 404
    response = client.get('/edit_client/1')
    assert response.status_code == 200
    response = client.get(('/edit_client/999'), follow_redirects=True)
    assert response.request.path == '/clients'

def test_random_route(client):
    response = client.get('/vfdvdf')
    assert response.status_code == 404
