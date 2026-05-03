import sys
from unittest.mock import MagicMock

# Mock flask so we can import app without installing it in the test environment
sys.modules['flask'] = MagicMock()

from app import Blockchain

def test_chain_valid_true():
    blockchain = Blockchain()

    # Create block 2
    previous_block = blockchain.print_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    blockchain.create_block(proof, previous_hash)

    # Create block 3
    previous_block = blockchain.print_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    blockchain.create_block(proof, previous_hash)

    # The chain should be valid
    assert blockchain.chain_valid(blockchain.chain) is True

def test_chain_valid_invalid_hash():
    blockchain = Blockchain()

    # Create block 2
    previous_block = blockchain.print_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    blockchain.create_block(proof, previous_hash)

    # Mess up the previous_hash of the second block
    blockchain.chain[1]['previous_hash'] = "invalid_hash_value"

    # The chain should now be invalid
    assert blockchain.chain_valid(blockchain.chain) is False

def test_chain_valid_invalid_proof():
    blockchain = Blockchain()

    # Create block 2
    previous_block = blockchain.print_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    blockchain.create_block(proof, previous_hash)

    # Create block 3
    previous_block = blockchain.print_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    blockchain.create_block(proof, previous_hash)

    # Mess up the proof of the second block
    blockchain.chain[1]['proof'] = 12345

    # The chain should now be invalid because the hash of proof^2 - previous_proof^2 won't have 5 leading zeros
    assert blockchain.chain_valid(blockchain.chain) is False
