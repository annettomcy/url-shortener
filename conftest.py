#pytest looks for this specificly named file
import pytest
from urlshort import create_app

#fixtures help establish testing situations
@pytest.fixture
def app():
    app = create_app()
    yield app

#fixture to get a client so testing framwework can act as a if it is a browser and test he project for us
@pytest.fixture
def client(app):
    return app.test_client()