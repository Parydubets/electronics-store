from store import create_app
from sqlalchemy_utils import database_exists
import os

def test_db_cnnection():
    db_user = os.environ.get('DB_USER')
    db_user = str(db_user)+':'
    db_password = os.environ.get('DB_PASSWORD')
    db_host = os.environ.get('DB_HOST')
    if db_password == '':
        db_user=db_user[0:-1]
    assert database_exists('mysql://{}{}@{}/store'.format(db_user,db_password,db_host))
    #assert database_exists('mysql://root:admin@localhost:3306/store')
    #assert database_exists('mysql://root@127.0.0.1:3306/store')
