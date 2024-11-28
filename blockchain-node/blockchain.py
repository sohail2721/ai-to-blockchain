import hashlib
import time
from flask import Flask, request, jsonify
from datetime import datetime
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
    data = request.get_json()
    
    # Print incoming request data in a structured manner
    print("\n--- Validating Result ---")
    print(f"Received data: {data}")
    
    result = data['result']
    broadcasted_at = data['timestamp']
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Simple validation logic to check if the result format is correct
    if isinstance(result['coefficients'], list) and isinstance(result['intercept'], (int, float)):
        # Store the result with timestamp to track when the node received it
        pending_transactions.append({
            'result': result,
            'received_at': current_time,
            'broadcasted_at': broadcasted_at
        })
        
        print(f"\nNode received the result at {current_time}, broadcasted at {broadcasted_at}")
        
        # Check if this is the first result or validate based on your own conditions
        if len(pending_transactions) > 1:  # Create a block if multiple transactions are received
            block = create_block(blockchain[-1]['hash'] if blockchain else '0')
            blockchain.append(block)
            pending_transactions.clear()  # Clear transactions after block creation
            
             # Pretty print the current blockchain
            print("\n--- Block Created ---")
            print("New block created:")
            print(f"  Index: {block['index']}")
            print(f"  Timestamp: {block['timestamp']}")
            print(f"  Previous Hash: {block['previous_hash']}")
            print(f"  Hash: {block['hash']}")
            print(f"  Transactions:")
            for tx in block['transactions']:
                print(f"    - Result: {tx['result']}")
                print(f"      Received At: {tx['received_at']}")
                print(f"      Broadcasted At: {tx['broadcasted_at']}")
                
            print("\nCurrent Blockchain:")
            for b in blockchain:
                print(f"\nBlock {b['index']}:")
                print(f"  Timestamp: {b['timestamp']}")
                print(f"  Previous Hash: {b['previous_hash']}")
                print(f"  Hash: {b['hash']}")
                print(f"  Transactions:")
                for tx in b['transactions']:
                    print(f"    - Result: {tx['result']}")
                    print(f"      Received At: {tx['received_at']}")
                    print(f"      Broadcasted At: {tx['broadcasted_at']}")
        
        return jsonify({"status": "valid", "block": blockchain[-1]}), 200
    else:
        print("\nInvalid result format received.")
        return jsonify({"status": "invalid"}), 400
    c
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
