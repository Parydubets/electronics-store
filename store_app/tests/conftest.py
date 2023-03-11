""" The conftest file """
import pytest
from store import create_app

@pytest.fixture
def app():
    """ The app test initiation """
    app = create_app({
        'TESTING': True,
    })

    yield app


@pytest.fixture
def client(app):
    """ App test client """
    return app.test_client()


@pytest.fixture()
def runner(app):
    """ Initiate cli_runner """
    return app.test_cli_runner()


def test_hello_command(runner):
    """ Hello test """
    result = runner.invoke(args="seed")
    print(result.output)
    assert "successfully" in result.output
