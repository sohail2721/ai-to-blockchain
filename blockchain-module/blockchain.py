import hashlib
import json
import os
import time

class Block:
    def __init__(self, index, previous_hash, data, timestamp):
        self.index = index
        self.previous_hash = previous_hash
        self.data = data
        self.timestamp = timestamp
        self.nonce = 0

    def compute_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    difficulty = 2

    def __init__(self):
        self.chain = []
        self.unconfirmed_data = []

    def create_genesis_block(self):
        genesis_block = Block(0, "0", {}, time.time())
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)

    def proof_of_work(self, block):
        block.nonce = 0
        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * Blockchain.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()
        return computed_hash

    def add_block(self, block, proof):
        last_block = self.chain[-1]
        if last_block.hash != block.previous_hash:
            return False
        if not self.is_valid_proof(block, proof):
            return False
        block.hash = proof
        self.chain.append(block)
        return True

    def is_valid_proof(self, block, block_hash):
        return block_hash.startswith('0' * Blockchain.difficulty) and block_hash == block.compute_hash()

# Initialize blockchain
blockchain = Blockchain()
blockchain.create_genesis_block()

# Load AI output

# Load AI output from shared volume
ai_output_path = "/shared-data/output.json"
if not os.path.exists(ai_output_path):
    raise FileNotFoundError("AI output file not found!")

with open(ai_output_path, "r") as f:
    ai_output = json.load(f)

print("AI Output Loaded for Blockchain Processing:", ai_output)

# Create new block
new_block = Block(index=len(blockchain.chain),
                  previous_hash=blockchain.chain[-1].compute_hash(),
                  data=data,
                  timestamp=time.time())

proof = blockchain.proof_of_work(new_block)
blockchain.add_block(new_block, proof)

print("Blockchain:", [block.__dict__ for block in blockchain.chain])
