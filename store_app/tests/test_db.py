from store import create_app
from sqlalchemy_utils import database_exists

def test_db_cnnection():
    assert database_exists('mysql://root@127.0.0.1:3306/store')
