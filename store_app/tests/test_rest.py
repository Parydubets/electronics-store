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
    print(f"######  {response.data}  ######")
    assert response.status_code == 400
    response = client.post('/api/clients_list', data={'first_name': 'Tony', \
                                                    'last_name': 'Stark',\
                                                    'phone':'+123456123459', \
                                                    'email': 'theironm1an@gmail.com', \
                                                    'date': '2023-01-30'})
    print(f"######  {response.data}  ######")
    assert response.status_code == 400
    


def test_get_client(client):
    response = client.get('/api/client/1')
    assert response.status_code == 200

def test_edit_client(client):
    response = client.put('api/client/1', data={'first_name':'Mike'})
    assert response.status_code == 200
    response = client.put('api/client/1', data={'phone': '1234567890123543'})
    assert response.status_code == 400
    response = client.put('api/client/1', data={'phone': '1'})
    assert response.status_code == 400

def test_delete_clint(client):
    response = client.delete('api/client/1')
    assert response.status_code == 200
    response = client.delete('api/client/1')
    assert response.status_code == 400
    response = client.delete('api/client/999')
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