import pytest
import json
from app import app, blockchain

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_mine_block_post(client):
    # Check the initial chain length
    initial_length = len(blockchain.chain)

    # Send a POST request to /mine_block
    response = client.post('/mine_block')

    assert response.status_code == 200

    response_data = json.loads(response.data)
    assert response_data['message'] == 'A block is MINED'
    assert 'index' in response_data
    assert response_data['index'] == initial_length + 1

    # Verify the chain actually grew
    assert len(blockchain.chain) == initial_length + 1

def test_mine_block_get_not_allowed(client):
    # Send a GET request to /mine_block
    response = client.get('/mine_block')

    # Should not be allowed since we changed it to POST only
    assert response.status_code == 405
