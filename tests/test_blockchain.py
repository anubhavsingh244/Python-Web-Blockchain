import sys
import hashlib
from unittest.mock import MagicMock

# Mock flask module completely
flask_mock = MagicMock()

class MockApp:
    def route(self, *args, **kwargs):
        def decorator(f):
            return f
        return decorator
    def run(self, *args, **kwargs):
        pass

flask_mock.Flask = lambda name: MockApp()
flask_mock.jsonify = lambda x: x
flask_mock.render_template = lambda *args, **kwargs: ""
flask_mock.url_for = lambda *args, **kwargs: ""

sys.modules['flask'] = flask_mock

from app import Blockchain

def test_proof_of_work_basic():
    """Test proof of work with the initial block's proof."""
    blockchain = Blockchain()
    previous_proof = 1
    new_proof = blockchain.proof_of_work(previous_proof)

    # Verify the proof generates a valid hash
    hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
    assert hash_operation[:5] == '00000'

def test_proof_of_work_different_previous():
    """Test proof of work with an arbitrary previous proof."""
    blockchain = Blockchain()
    previous_proof = 533
    new_proof = blockchain.proof_of_work(previous_proof)

    # Verify the proof generates a valid hash
    hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
    assert hash_operation[:5] == '00000'
