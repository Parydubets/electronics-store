import pytest
from store import create_app
import click


@pytest.fixture
def app():

    app = create_app({
        'TESTING': True,
    })

    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


def test_hello_command(runner):
    result = runner.invoke(args="seed")
    assert "successfully" in result.output