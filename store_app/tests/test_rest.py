import os
from flask  import request
from sqlalchemy_utils import database_exists, drop_database, create_database
from store.rest import *
from sqlalchemy_utils import database_exists, drop_database, create_database

def test_get_clients(client):
    response = client.get('/api/clients_list')
    assert response.status_code == 200
"""    #assert response.data == jsonify(clients_schema.dump(get_clients_list(False)))
    print("deump: ",f'b{(str(clients_schema.dump(get_clients_list(False))))}')
    print()
    print("load: ",response.data[0:-1])
    assert f'b{(str(clients_schema.dump(get_clients_list(False))))}' == response.data[0:-1]"""

def test_post_clients(client):
    response = client.post('/api/clients_list', data={'first_name': 'Tony', \
                                                    'last_name': 'Stark',\
                                                    'phone':'+123456123459', \
                                                    'email': 'theironman@gmail.com', \
                                                    'date': '2023-01-30'})
    assert response.status_code == 201
    response = client.post('/api/clients_list', data={'first_name': 'Tony', \
                                                    'last_name': 'Stark',\
                                                    'phone':'+123456123454', \
                                                    'email': 'theironman@gmail.com', \
                                                    'date': '2023-01-30'})
    assert response.status_code == 400
    response = client.post('/api/clients_list', data={'first_name': 'Tony', \
                                                    'last_name': 'Stark',\
                                                    'phone':'+123456123459', \
                                                    'email': 'theironm1an@gmail.com', \
                                                    'date': '2023-01-30'})
    assert response.status_code == 400
    response = client.post('/api/clients_list', data={'first_name': 'Tony', \
                                                      'last_name': 'Stark', \
                                                      'phone': '+12345', \
                                                      'email': 'theironm1an@gmail.com', \
                                                      'date': '2023-01-30'})
    assert response.status_code == 400
    response = client.post('/api/clients_list', data={'first_name': 'Tony', \
                                                      'last_name': 'Stark', \
                                                      'phone': '+1233452345656456345', \
                                                      'email': 'theironm1an@gmail.com', \
                                                      'date': '2023-01-30'})
    assert response.status_code == 400
    


def test_get_client(client):
    response = client.get('/api/client/1')
    assert response.status_code == 200
    response = client.get('/api/client/999')
    assert response.status_code == 400

def test_edit_client(client):
    response = client.put('api/client/1', data={'first_name':'Mike', 'last_name':'Vasovski'})
    assert response.status_code == 200
    response = client.put('api/client/1', data={'phone': '1234567890123543'})
    assert response.status_code == 400
    response = client.put('api/client/1', data={'phone': '+123456123425'})
    assert response.status_code == 200
    response = client.put('api/client/1', data={'email': 'someone@gmail.com'})
    assert response.status_code == 200
    response = client.put('api/client/1', data={'email': 'someone@gmail.com'})
    assert response.status_code == 400
    response = client.put('api/client/1', data={'phone': '1'})
    assert response.status_code == 400
    response = client.put('api/client/999', data={'phone': '1'})
    assert response.status_code == 400

def test_delete_clint(client):
    response = client.delete('api/client/1')
    assert response.status_code == 200
    response = client.delete('api/client/1')
    assert response.status_code == 400
    response = client.delete('api/client/999')
    assert response.status_code == 400


def test_get_orders(client):
    response = client.get('/api/orders_list')
    assert response.status_code == 200

def test_post_orders(client):
    response = client.post('/api/orders_list', data={'full_name': 'Tony Stark', \
                                                     'phone': '+123456123459', \
                                                     'order': 'Smartphone Q2',\
                                                    'address': '10501 Wrangler Way, Corona, CA 92883, USA', \
                                                    'date': '2023-01-30'})
    assert response.status_code == 201
    response = client.post('/api/orders_list', data={'full_name': 'Tony Star', \
                                                    'order': 'Smartphone Q2',\
                                                    'phone':'+123456123459', \
                                                    'address': '10501 Wrangler Way, Corona, CA 92883, USA', \
                                                    'date': '2023-01-30'})
    assert response.status_code == 400
    response = client.post('/api/orders_list', data={'full_name': 'Tony Stark', \
                                                    'order': 'Smartphone Q2',\
                                                    'phone':'+123456123452', \
                                                    'address': '10501 Wrangler Way, Corona, CA 92883, USA', \
                                                    'date': '2023-01-30'})
    assert response.status_code == 400
    response = client.post('/api/orders_list', data={'full_name': 'Tony Stark', \
                                                    'order': 'Smartphone Q2',\
                                                    'phone':'+123456123452ds', \
                                                    'address': '10501 Wrangler Way, Corona, CA 92883, USA', \
                                                    'date': '2023-01-30'})
    assert response.status_code == 400
    response = client.post('/api/orders_list', data={'full_name': 'Tony Stark', \
                                                    'order': 'Smartphone Q2, Smartphone Q2',\
                                                    'phone':'+123456123452', \
                                                    'address': '10501 Wrangler Way, Corona, CA 92883, USA', \
                                                    'date': '2023-01-30'})
    assert response.status_code == 400
    response = client.post('/api/orders_list', data={'full_name': 'Tony Stark', \
                                                     'order': 'sdfvsdf', \
                                                     'phone': '+123456123452', \
                                                     'address': '10501 Wrangler Way, Corona, CA 92883, USA', \
                                                     'date': '2023-01-30'})
    assert response.status_code == 400
    client.put('api/product/2', data={'amount': '0'})
    response = client.post('/api/orders_list', data={'full_name': 'Tony Stark', \
                                                     'order': 'Smartphone Q2, Laptop SM234', \
                                                     'phone': '+123456123452', \
                                                     'address': '10501 Wrangler Way, Corona, CA 92883, USA', \
                                                     'date': '2023-01-30'})
    assert response.status_code == 400


def test_get_order(client):
    response = client.get('/api/order/1')
    assert response.status_code == 200
    response = client.get('/api/order/999')
    assert response.status_code == 400


def test_edit_order(client):
    response = client.put('api/order/1', data={'full_name':'Mike Stevenson'})
    assert response.status_code == 400
    response = client.put('api/order/1', data={'order': 'Smartphone Q2, Smartphone Q2'})
    assert response.status_code == 400
    response = client.put('api/order/1', data={'order': 'Smartphone Q2, Laptop SM234, Laptop SM234'})
    assert response.status_code == 400
    response = client.put('api/order/1', data={'phone': '+123456123453'})
    assert response.status_code == 400
    response = client.put('api/order/1', data={'date': '2020-12-01'})
    assert response.status_code == 200
    response = client.put('api/order/1', data={'address': 'Browning st.'})
    assert response.status_code == 200
    response = client.put('api/order/999', data={'address': 'Browning st.'})
    assert response.status_code == 400

def test_delete_order(client):
    response = client.delete('api/order/1')
    assert response.status_code == 200
    response = client.delete('api/order/1')
    assert response.status_code == 400
    response = client.delete('api/order/999')
    assert response.status_code == 400


def test_get_products(client):
    response = client.get('/api/products_list')
    assert response.status_code == 200

def test_get_product(client):
    response = client.get('/api/product/1')
    assert response.status_code == 200
    response = client.get('/api/product/999')
    assert response.status_code == 400

def test_post_products(client):
    response = client.post('/api/products_list', data={'name': 'Powerbank 10000 mAh', \
                                                     'year': '2020', \
                                                     'cost': '50',\
                                                    'amount': '20', \
                                                    'category': 'Powerbanks'})
    assert response.status_code == 201
    response = client.post('/api/products_list', data={'name': 'Powerbank 10000 mAh', \
                                                     'year': '2020', \
                                                     'cost': '50',\
                                                    'amount': '20', \
                                                    'category': 'Powerbanks'})
    assert response.status_code == 400


def test_edit_product(client):
    response = client.put('api/product/1', data={'name':'Pro Powerbank 10000 mAh'})
    assert response.status_code == 200
    response = client.put('api/product/1', data={'category': 'Pro Powerbanks'})
    assert response.status_code == 200
    response = client.put('api/product/1', data={'price': '75'})
    assert response.status_code == 200
    response = client.put('api/product/1', data={'amount': '20'})
    assert response.status_code == 200
    response = client.put('api/product/1', data={'year': '2020'})
    assert response.status_code == 200
    response = client.put('api/product/999', data={'phone': '1'})
    assert response.status_code == 400


def test_delete_product(client):
    response = client.delete('api/product/1')
    assert response.status_code == 200
    response = client.delete('api/product/1')
    assert response.status_code == 400
    response = client.delete('api/product/999')
    assert response.status_code == 400

def test_clients_orders(client):
    response = client.get('api/orders_list/client/2')
    assert response.status_code == 200
    response = client.get('api/orders_list/client/999')
    assert response.status_code == 400

def test_get_sum(client):
    response = client.get('/api/orders/sum')
    assert response.status_code == 200

def test_get_sum_by_client(client):
    response = client.get('/api/client/2/sum')
    assert response.status_code == 200
    response = client.get('/api/client/999/sum')
    assert response.status_code == 400

def test_last_rest_test(client):
    os.environ['FLASK_APP']='store'
    db_user = os.environ['DB_USER']
    db_password = os.environ['DB_PASSWORD']
    db_host = os.environ['DB_HOST']
    if db_password != '':
        db_user += ':'
    database = 'mysql://{}{}@{}/store'.format(db_user, db_password, db_host)
    if database_exists(database):
        drop_database(database)

    create_database(database)
    os.system("flask db upgrade")
    os.system("flask db migrate")
    os.system("flask db upgrade")
    os.system("flask seed")