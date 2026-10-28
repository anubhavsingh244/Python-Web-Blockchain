import sys
import datetime
import hashlib
import pytest
from unittest.mock import MagicMock

@pytest.fixture(autouse=True)
def mock_flask(monkeypatch):
    """Mock flask because it's not installed in the isolated environment where pytest runs."""
    flask_mock = MagicMock()
    def route_mock(*args, **kwargs):
        def decorator(f):
            return f
        return decorator

    flask_mock.Flask.return_value.route = route_mock
    flask_mock.jsonify = lambda x: x
    flask_mock.render_template = lambda *args, **kwargs: ""
    flask_mock.url_for = lambda *args, **kwargs: ""

    monkeypatch.setitem(sys.modules, 'flask', flask_mock)

    # Also we need to import Blockchain inside the test or yield to allow app.py to import the mocked flask
    # If we import at the top level, it fails because fixture is not yet applied
    # Let's yield and then the test can import, or better, we just reload the module if necessary.
    # Actually, importing inside the test function works best to ensure it imports with the mock.
    yield

def test_create_block_increases_length():
    """Test that creating a block increases the chain length."""
    from app import Blockchain
    b = Blockchain()
    initial_length = len(b.chain)

    b.create_block(proof=100, previous_hash='abc123def')

    assert len(b.chain) == initial_length + 1

def test_create_block_attributes():
    """Test that the block created has the correct attributes."""
    from app import Blockchain
    b = Blockchain()

    # create_block is already called once in __init__ (genesis block)
    block = b.create_block(proof=123, previous_hash='some_hash')

    assert block['index'] == 2
    assert block['proof'] == 123
    assert block['previous_hash'] == 'some_hash'

    # check that timestamp is valid
    try:
        datetime.datetime.strptime(block['timestamp'], '%Y-%m-%d %H:%M:%S.%f')
    except ValueError:
        # Some platforms might not have microseconds if it's exact, fallback
        try:
            datetime.datetime.strptime(block['timestamp'], '%Y-%m-%d %H:%M:%S')
        except ValueError:
            assert False, f"Invalid timestamp format: {block['timestamp']}"

    assert b.chain[-1] == block

def test_create_multiple_blocks():
    """Test creating multiple blocks successively."""
    from app import Blockchain
    b = Blockchain()

    b.create_block(proof=10, previous_hash='hash1')
    b.create_block(proof=20, previous_hash='hash2')
    b.create_block(proof=30, previous_hash='hash3')

    assert len(b.chain) == 4  # 1 genesis + 3 new
    assert b.chain[1]['proof'] == 10
    assert b.chain[2]['proof'] == 20
    assert b.chain[3]['proof'] == 30

    assert b.chain[1]['previous_hash'] == 'hash1'
    assert b.chain[2]['previous_hash'] == 'hash2'
    assert b.chain[3]['previous_hash'] == 'hash3'

def test_proof_of_work_basic():
    """Test proof of work with the initial block's proof."""
    from app import Blockchain
    b = Blockchain()
    previous_proof = 1
    new_proof = b.proof_of_work(previous_proof)

    # Verify the proof generates a valid hash
    hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
    assert hash_operation[:5] == '00000'

def test_proof_of_work_different_previous():
    """Test proof of work with an arbitrary previous proof."""
    from app import Blockchain
    b = Blockchain()
    previous_proof = 533
    new_proof = b.proof_of_work(previous_proof)

    # Verify the proof generates a valid hash
    hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
    assert hash_operation[:5] == '00000'

def _build_chain(blocks=2):
    """Return a Blockchain with `blocks` valid mined blocks after genesis."""
    from app import Blockchain
    bc = Blockchain()
    for _ in range(blocks):
        prev_block = bc.print_previous_block()
        proof = bc.proof_of_work(prev_block['proof'])
        bc.create_block(proof, bc.hash(prev_block))
    return bc

def test_chain_valid_returns_true_for_valid_chain():
    bc = _build_chain()
    assert bc.chain_valid(bc.chain) is True

def test_chain_valid_returns_false_for_corrupted_hash():
    bc = _build_chain()
    # Corrupt the previous_hash reference in block 1
    bc.chain[1]['previous_hash'] = 'corrupted_hash'
    assert bc.chain_valid(bc.chain) is False

def test_chain_valid_returns_false_for_corrupted_proof():
    bc = _build_chain()
    # Corrupt the proof in block 1 so hash operation won't start with 00000
    bc.chain[1]['proof'] = 123456789
    assert bc.chain_valid(bc.chain) is False

def test_chain_valid_returns_false_for_mutated_previous_block_data():
    bc = _build_chain()
    # Mutating block 0 changes its hash, so block 1's previous_hash no longer matches
    bc.chain[0]['proof'] = 999
    assert bc.chain_valid(bc.chain) is False
