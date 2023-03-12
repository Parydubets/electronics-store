from flask  import request, url_for, current_app, session
from store import create_app
from store.views import *
from store.models import Product
from store.service import get_item_with_filter

def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing

def test_clients_route(client):
    response = client.get('/')
    assert response.status_code == 200
    response = client.get('/clients')
    assert response.status_code == 200

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
    response = client.get('/edit_product')
    assert response.status_code == 404
    response = client.get('/edit_product/1')
    assert response.status_code == 200
    response = client.get(('/edit_product/999'), follow_redirects=True)
    assert response.request.path == '/products'
    response = client.post('/edit_order/1', data = {'full_name': 'Peter Parker',\
                                                   'phone': '+123456123450',\
                                                   'order' : 'Smartphone Q2, Laptop SM234',\
                                                   'address' : '20 Ingram Street, NY, NY, USA',\
                                                   'date' : '2023-01-30'})
    assert response.status_code == 302
    assert response.headers['Location'] == '/orders'
    response = client.post('/edit_order/1', data={'full_name': 'Peter Parkerr', \
                                                  'phone': '+123456123458', \
                                                  'order': 'Smartphone Q2, Laptop SM234', \
                                                  'address': '20 Ingram Street, NY, NY, US', \
                                                  'date': '2023-01-26'})
    assert response.status_code == 200
    response = client.post('/edit_order/1', data={'full_name': 'Peter Parker', \
                                                  'phone': '+123456123450', \
                                                  'order': 'Smartphone Q2, Laptop SM2', \
                                                  'address': '20 Ingram Street, NY, NY, USA', \
                                                  'date': '2023-01-30'})
    assert response.status_code == 302
    assert response.headers['Location'] == '/edit_order/1'

def test_delete_product_route(client):
    response = client.get('/delete_product/1')
    assert response.status_code == 200
    response = client.post('/delete_product/999', data={'submit': True})
    assert response.status_code == 302
    assert response.headers['Location'] == '/products'

def test_random_route(client):
    response = client.get('/vfdvdf')
    assert response.status_code == 404

def test_validate_order(client):
    with client.application.app_context():
        product = get_item_with_filter(Product, Product.id, 1)
        response = views.validate_order("Smartphone Q2", product)
        assert response == True

