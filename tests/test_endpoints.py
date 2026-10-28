import pytest
from app import app, blockchain


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def fresh_chain():
    """Reset the shared module-level blockchain, then restore it afterwards."""
    saved = list(blockchain.chain)
    blockchain.chain = []
    blockchain.create_block(proof=1, previous_hash='0')
    yield blockchain
    blockchain.chain = saved


@pytest.mark.parametrize('path', ['/', '/display_block', '/display_chain'])
def test_html_pages_render(client, path):
    response = client.get(path)
    assert response.status_code == 200
    assert b'<html' in response.data.lower()


def test_mine_block_response_shape(client, fresh_chain):
    response = client.post('/mine_block')
    assert response.status_code == 200

    data = response.get_json()
    assert data['message'] == 'A block is MINED'
    assert data['index'] == 2
    assert isinstance(data['timestamp'], str)
    assert isinstance(data['proof'], int)
    assert data['previous_hash'] == fresh_chain.hash(fresh_chain.chain[0])


def test_mine_block_links_to_previous_block(client, fresh_chain):
    client.post('/mine_block')
    client.post('/mine_block')

    assert len(fresh_chain.chain) == 3
    for prev, block in zip(fresh_chain.chain, fresh_chain.chain[1:]):
        assert block['previous_hash'] == fresh_chain.hash(prev)


def test_is_valid_true_after_mining(client, fresh_chain):
    client.post('/mine_block')

    response = client.get('/is_valid')
    assert response.status_code == 200
    assert response.get_json() == {'message': 'The Blockchain is valid.'}


def test_is_valid_false_for_tampered_chain(client, fresh_chain):
    client.post('/mine_block')
    fresh_chain.chain[0]['proof'] = 999

    response = client.get('/is_valid')
    assert response.status_code == 200
    assert response.get_json() == {'message': 'The Blockchain is not valid.'}


def test_get_chain_reflects_mined_blocks(client, fresh_chain):
    client.post('/mine_block')

    data = client.get('/get_chain').get_json()
    assert data['length'] == 2
    assert [b['index'] for b in data['chain']] == [1, 2]
