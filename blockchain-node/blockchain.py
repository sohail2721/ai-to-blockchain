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

@app.route('/test_connection', methods=['GET'])
def test_connection():
    # You can just return a simple status for the test
    return jsonify({"status": "Connection successful!"}), 200


@app.route('/validate_result', methods=['POST'])
def validate_result():
    # Get the JSON data from the request
    data = request.get_json()

    # Check if the data contains the necessary fields
    if not data or 'coefficients' not in data or 'intercept' not in data:
        return jsonify({"error": "Invalid data structure"}), 400

    print(f"Validating result: {data}")
    
    # Simple validation of the result
    if isinstance(data['coefficients'], list) and isinstance(data['intercept'], (int, float)):
        # Add the result to pending transactions
        pending_transactions.append(data)

        # If there are enough transactions, create a new block
        if len(pending_transactions) > 1:  # Simple condition for block creation
            prev_hash = blockchain[-1]['hash'] if blockchain else '0'
            block = create_block(prev_hash)
            blockchain.append(block)
            pending_transactions.clear()  # Clear transactions after block creation

        # Check if blockchain has at least one block before returning it
        if blockchain:
            return jsonify({"status": "valid", "block": blockchain[-1]}), 200
        else:
            # If no block is created yet, return a message
            return jsonify({"status": "valid", "message": "No block created yet"}), 200

    # If the validation fails, return an error message
    else:
        return jsonify({"status": "invalid"}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
