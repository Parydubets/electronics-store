""" The conftest file """
import pytest
from store import create_app

@pytest.fixture
def app():
    """ The app test initiation """
    app = create_app({
        'TESTING': True,
    })
    with app.app_context():
        app.config['WTF_CSRF_ENABLED'] = False
        yield app


@pytest.fixture
def client(app):
    """ App test client """
    return app.test_client()

