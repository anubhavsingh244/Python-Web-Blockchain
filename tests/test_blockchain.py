import sys
import datetime
from unittest.mock import MagicMock

# Mock flask because it's not installed in the isolated environment where pytest runs
flask_mock = MagicMock()
def route_mock(*args, **kwargs):
    def decorator(f):
        return f
    return decorator

flask_mock.Flask.return_value.route = route_mock
flask_mock.jsonify = lambda x: x
flask_mock.render_template = lambda *args, **kwargs: ""
flask_mock.url_for = lambda *args, **kwargs: ""

sys.modules['flask'] = flask_mock

from app import Blockchain

def test_create_block_increases_length():
    """Test that creating a block increases the chain length."""
    b = Blockchain()
    initial_length = len(b.chain)

    b.create_block(proof=100, previous_hash='abc123def')

    assert len(b.chain) == initial_length + 1

def test_create_block_attributes():
    """Test that the block created has the correct attributes."""
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
