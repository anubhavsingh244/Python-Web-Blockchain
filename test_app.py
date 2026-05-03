import app

def test_blockchain():
    blockchain = app.Blockchain()

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

    is_valid = blockchain.chain_valid(blockchain.chain)
    print(f"Chain is valid: {is_valid}")
    assert is_valid == True, "Blockchain should be valid"

if __name__ == "__main__":
    test_blockchain()
    print("All tests passed!")