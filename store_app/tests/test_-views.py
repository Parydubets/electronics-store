from flask  import request,get_flashed_messages
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
    response = client.get('/clients?date_from=2022-12-31&date_to=2023-03-12&refresh=Filter')
    assert response.status_code == 200
    response = client.get('/clients?date_from=2002-12-31&date_to=2003-03-12&refresh=Filter')
    assert response.status_code == 200

def test_new_client_route(client):
    response = client.get('/new_client')
    assert response.status_code == 200
    response = client.post('/new_client', data={'cancel': True})
    assert response.status_code == 302
    response = client.post('/new_client', data={'submit': True, 'first_name':'Harry',\
                                                'last_name':'Potter',\
                                                'email':'harrypotter@hmail.com',\
                                                'phone':'+445332445678'})
    assert response.status_code == 302
    response = client.post('/new_client', data={'submit': True, 'first_name': 'Harry', \
                                                'last_name': 'Potter', \
                                                'email': 'harrypotter@hmail.com', \
                                                'phone': '+445332445674'})
    assert response.status_code == 200
    response = client.post('/new_client', data={'submit': True, 'first_name': 'Harry', \
                                                'last_name': 'Potter', \
                                                'email': 'harrypotter@gmail.com', \
                                                'phone': '+445332445678'})
    assert response.status_code == 200


def test_edit_client_route(client):
    response = client.get('/edit_client')
    assert response.status_code == 404
    response = client.post('/edit_client/1')
    assert response.status_code == 200
    response = client.get('/edit_client/4', data={'cancel' : True, 'first_name': 'Harry'})
    assert response.status_code == 200
    response = client.post('/edit_client/4', data={'cancel' : True, 'first_name': 'Harry'})
    assert response.status_code == 302
    response = client.post('/edit_client/1', data={'submit': True, 'first_name': 'Harry', \
                                                'last_name': 'Potter', \
                                                'email': 'harrypotter@gmail.com', \
                                                'phone': '+445332445678'})
    assert response.status_code == 302
    response = client.post(('/edit_client/999'), follow_redirects=True)
    assert response.request.path == '/clients'

def test_delete_client(client):
    response = client.get('/delete_client/1')
    assert response.status_code == 200
    response = client.post('/delete_client/999', data={'submit': True})
    assert response.status_code == 302
    assert response.headers['Location'] == '/clients'
    response = client.post('/delete_client/1', data={'cancel': True})
    assert response.status_code == 302
    assert response.headers['Location'] == '/clients'
    response = client.post('/delete_client/4', data={'submit': True})
    assert response.status_code == 302
    assert response.headers['Location'] == '/clients'

def test_orders_route(client):
    response = client.get('/orders')
    assert response.status_code == 200



def test_new_order_route(client):
    response = client.get('/new_order')
    assert response.status_code == 200
    with client.application.app_context():
        response = client.post('/new_order', data={'submit':True,'full_name': 'Tony Stark', \
                                                         'phone': '+123456123459', \
                                                         'order': 'Smartphone Q2', \
                                                         'address': '10501 Wrangler Way, Corona, CA 92883, USA', \
                                                         'date': '2023-01-30'})
        assert response.status_code == 200
        response = client.post('/new_order', data={'submit':True,'full_name': 'Tony Stark', \
                                                         'order': 'Smartphone Q2', \
                                                         'phone': '+123456123452', \
                                                         'address': '10501 Wrangler Way, Corona, CA 92883, USA', \
                                                         'date': '2023-01-30'})
        assert response.status_code == 200
        response = client.post('/new_order', data={'submit':True,'full_name': 'Tony Stark', \
                                                         'order': 'Smartphone Q2', \
                                                         'phone': '+123456123452ds', \
                                                         'address': '10501 Wrangler Way, Corona, CA 92883, USA', \
                                                         'date': '2023-01-30'})
        assert response.status_code == 200
        response = client.post('/new_order', data={'submit':True,'full_name': 'Tony Stark', \
                                                         'order': 'Smartphone Q2, Smartphone Q2', \
                                                         'phone': '+123456123452', \
                                                         'address': '10501 Wrangler Way, Corona, CA 92883, USA', \
                                                         'date': '2023-01-30'})
        assert response.status_code == 200
        response = client.post('/new_order', data={'submit':True,'full_name': 'Tony Stark', \
                                                         'order': 'sdfvsdf', \
                                                         'phone': '+123456123452', \
                                                         'address': '10501 Wrangler Way, Corona, CA 92883, USA', \
                                                         'date': '2023-01-30'})
        response = client.post('/new_order', data={'cancel':True,'full_name': 'Tony Stark', \
                                                         'order': 'sdfvsdf', \
                                                         'phone': '+123456123452', \
                                                         'address': '10501 Wrangler Way, Corona, CA 92883, USA', \
                                                         'date': '2023-01-30'})
        assert response.status_code == 302
        response = client.get('/new_order', data={'submit':'True','full_name': 'Tony Stark', \
                                                         'order': 'Smartphone Q2, Laptop SM234', \
                                                         'phone': '+123456123452', \
                                                         'address': '10501 Wrangler Way, Corona, CA 92883, USA', \
                                                         'date': '2023-01-30'})
        assert response.status_code == 200


def test_edit_order_route(client):
    response = client.get('/edit_order')
    assert response.status_code == 404
    response = client.get('/edit_order/1')
    assert response.status_code == 200
    response = client.get('/delete_order/1')
    assert response.status_code == 200
    response = client.get('/edit_order/1')
    assert response.status_code == 200
    response = client.get(('/edit_order/999'), follow_redirects=True)
    assert response.request.path == '/orders'

def test_delete_order(client):

    response = client.post('/delete_order/999', data={'submit': True})
    assert response.status_code == 302
    assert response.headers['Location'] == '/orders'
    response = client.post('/delete_order/1', data={'cancel': True})
    assert response.status_code == 302
    assert response.headers['Location'] == '/orders'
    response = client.post('/delete_order/4', data={'submit': True})
    assert response.status_code == 302
    assert response.headers['Location'] == '/orders'


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
    assert response.status_code == 200
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
    assert response.status_code == 200


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

