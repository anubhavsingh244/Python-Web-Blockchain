import sys
from unittest.mock import MagicMock
import json

# Mock flask module so app.py can be imported without it
flask_mock = MagicMock()
def route_mock(*args, **kwargs):
    def decorator(f):
        return f
    return decorator

flask_mock.Flask.return_value.route = route_mock
flask_mock.jsonify = lambda x: x
sys.modules['flask'] = flask_mock

from app import Blockchain

def test_chain_valid_returns_true_for_valid_chain():
    bc = Blockchain()
    # Add a couple of blocks to form a valid chain
    for i in range(2):
        prev_block = bc.print_previous_block()
        proof = bc.proof_of_work(prev_block['proof'])
        prev_hash = bc.hash(prev_block)
        bc.create_block(proof, prev_hash)

    assert bc.chain_valid(bc.chain) is True

def test_chain_valid_returns_false_for_corrupted_hash():
    bc = Blockchain()
    for i in range(2):
        prev_block = bc.print_previous_block()
        proof = bc.proof_of_work(prev_block['proof'])
        prev_hash = bc.hash(prev_block)
        bc.create_block(proof, prev_hash)

    # Corrupt the previous_hash reference in block 1
    bc.chain[1]['previous_hash'] = 'corrupted_hash'
    assert bc.chain_valid(bc.chain) is False

def test_chain_valid_returns_false_for_corrupted_proof():
    bc = Blockchain()
    for i in range(2):
        prev_block = bc.print_previous_block()
        proof = bc.proof_of_work(prev_block['proof'])
        prev_hash = bc.hash(prev_block)
        bc.create_block(proof, prev_hash)

    # Corrupt the proof in block 1 so hash operation won't start with 00000
    bc.chain[1]['proof'] = 123456789
    assert bc.chain_valid(bc.chain) is False

def test_chain_valid_returns_false_for_mutated_previous_block_data():
    bc = Blockchain()
    for i in range(2):
        prev_block = bc.print_previous_block()
        proof = bc.proof_of_work(prev_block['proof'])
        prev_hash = bc.hash(prev_block)
        bc.create_block(proof, prev_hash)

    # Corrupt data in block 0 so its hash changes
    # This will cause block 1's previous_hash to not match the hash of block 0
    bc.chain[0]['proof'] = 999
    assert bc.chain_valid(bc.chain) is False
