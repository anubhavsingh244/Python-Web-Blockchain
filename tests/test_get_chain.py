import pytest
from app import app, blockchain

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_chain(client):
    response = client.get('/get_chain')
    assert response.status_code == 200

    data = response.get_json()
    assert 'chain' in data
    assert 'length' in data

    assert data['length'] == len(blockchain.chain)
    assert data['chain'] == blockchain.chain
