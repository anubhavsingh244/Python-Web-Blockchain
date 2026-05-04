import sys
import datetime
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
