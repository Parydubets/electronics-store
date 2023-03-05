from store import create_app
from sqlalchemy_utils import database_exists
import os

def test_db_cnnection():
    db_user = os.environ.get('DB_USER')
    db_password = os.environ.get('DB_PASSWORD')
    db_host = os.environ.get('DB_HOST')
    print(db_user, db_password, db_host)
    #assert database_exists('mysql://{}:{}@{}/store'.format(db_user,db_password,db_host))
    assert database_exists('mysql://root@127.0.0.1:3306/store')
