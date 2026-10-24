import pytest
import server


@pytest.fixture(autouse=True)
def reset_server_data():
    server.reset_data()
    yield
    server.reset_data()


@pytest.fixture
def client():
    server.app.config['TESTING'] = True
    server.app.config['WTF_CSRF_ENABLED'] = False
    with server.app.test_client() as client:
        yield client
