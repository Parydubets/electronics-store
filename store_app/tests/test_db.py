from store import create_app
from sqlalchemy_utils import database_exists

def test_db_cnnection():
    assert database_exists('mysql://root:admin@localhost:3306/store')
