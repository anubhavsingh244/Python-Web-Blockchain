import pytest
import json
import hashlib
from app import app, Blockchain

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def clean_blockchain():
    from app import blockchain
    # Reset the blockchain before each test
    blockchain.chain = []
    blockchain.create_block(proof=1, previous_hash='0')
    return blockchain

def test_blockchain_initialization():
    b = Blockchain()
    assert len(b.chain) == 1
    assert b.chain[0]['index'] == 1
    assert b.chain[0]['previous_hash'] == '0'
    assert b.chain[0]['proof'] == 1

def test_create_block():
    b = Blockchain()
    initial_length = len(b.chain)
    block = b.create_block(proof=123, previous_hash='abc')

    assert len(b.chain) == initial_length + 1
    assert block['index'] == initial_length + 1
    assert block['proof'] == 123
    assert block['previous_hash'] == 'abc'
    assert block == b.chain[-1]

def test_print_previous_block():
    b = Blockchain()
    block = b.create_block(proof=123, previous_hash='abc')
    assert b.print_previous_block() == block

def test_proof_of_work():
    b = Blockchain()
    previous_proof = 1 # genesis block proof
    proof = b.proof_of_work(previous_proof)

    # Verify the hash starts with 00000
    hash_operation = hashlib.sha256(
        str(proof**2 - previous_proof**2).encode()
    ).hexdigest()
    assert hash_operation[:5] == '00000'

def test_hash():
    b = Blockchain()
    block = {'index': 1, 'proof': 1, 'previous_hash': '0', 'timestamp': '2023-01-01'}
    expected_hash = hashlib.sha256(json.dumps(block, sort_keys=True).encode()).hexdigest()
    assert b.hash(block) == expected_hash

def test_chain_valid():
    b = Blockchain()

    # Mine a valid block
    previous_block = b.print_previous_block()
    previous_proof = previous_block['proof']
    proof = b.proof_of_work(previous_proof)
    previous_hash = b.hash(previous_block)
    b.create_block(proof, previous_hash)

    assert b.chain_valid(b.chain) is True

def test_chain_invalid_previous_hash():
    b = Blockchain()

    previous_block = b.print_previous_block()
    previous_proof = previous_block['proof']
    proof = b.proof_of_work(previous_proof)
    # Give wrong hash
    b.create_block(proof, "wrong_hash")

    assert b.chain_valid(b.chain) is False

def test_chain_invalid_proof():
    b = Blockchain()

    previous_block = b.print_previous_block()
    previous_hash = b.hash(previous_block)
    # Give wrong proof
    b.create_block(12345, previous_hash)

    assert b.chain_valid(b.chain) is False

# Flask App Tests
def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200

def test_mine_block(client, clean_blockchain):
    initial_length = len(clean_blockchain.chain)
    response = client.get('/mine_block')

    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'A block is MINED'
    assert data['index'] == initial_length + 1
    assert len(clean_blockchain.chain) == initial_length + 1

def test_display_block(client):
    response = client.get('/display_block')
    assert response.status_code == 200

def test_get_chain(client, clean_blockchain):
    response = client.get('/get_chain')

    assert response.status_code == 200
    data = response.get_json()
    assert len(data['chain']) == len(clean_blockchain.chain)
    assert data['length'] == len(clean_blockchain.chain)

def test_display_chain(client):
    response = client.get('/display_chain')
    assert response.status_code == 200

def test_valid_endpoint(client, clean_blockchain):
    # Ensure chain is valid first
    response = client.get('/is_valid')
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'The Blockchain is valid.'

    # Break the chain to test the invalid branch
    client.get('/mine_block')
    clean_blockchain.chain[-1]['proof'] = -1
    response = client.get('/is_valid')
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'The Blockchain is not valid.'
