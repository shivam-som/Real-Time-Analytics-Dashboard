import pytest
from app import app
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as c:
        yield c

def test_health(client):
    rv = client.get('/api/health')
    assert rv.status_code == 200
    assert 'status' in rv.get_json()
