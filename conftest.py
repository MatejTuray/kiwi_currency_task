import pytest
from run import create_app


@pytest.fixture
def app():
    app = create_app("config")
    return app
