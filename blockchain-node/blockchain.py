import hashlib
import time
from flask import Flask, request, jsonify

app = Flask(__name__)

blockchain = []
pending_transactions = []

# Function to create a new block
def create_block(previous_hash):
    block = {
        "index": len(blockchain) + 1,
        "timestamp": time.time(),
        "transactions": pending_transactions,
        "previous_hash": previous_hash,
        "hash": hashlib.sha256(str(time.time()).encode('utf-8')).hexdigest()
    }
    return block

@app.route('/validate_result', methods=['POST'])
def validate_result():
    data = request.get_json()
    print(f"Validating result: {data}")
    
    # Simple validation of the result
    if isinstance(data['coefficients'], list) and isinstance(data['intercept'], (int, float)):
        # Add the result to pending transactions
        pending_transactions.append(data)
        if len(pending_transactions) > 1:  # Simple condition for block creation
            block = create_block(blockchain[-1]['hash'] if blockchain else '0')
            blockchain.append(block)
            pending_transactions.clear()  # Clear transactions after block creation
        return jsonify({"status": "valid", "block": blockchain[-1]}), 200
    else:
        return jsonify({"status": "invalid"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
