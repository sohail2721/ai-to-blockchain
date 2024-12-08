import hashlib
import time
from flask import Flask, request, jsonify
from datetime import datetime
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
app = Flask(__name__)

blockchain = []
pending_transactions = []

def proof_of_work(previous_hash, transactions, difficulty=4):
    nonce = 0
    while True:
        block_string = f"{previous_hash}{transactions}{nonce}"
        block_hash = hashlib.sha256(block_string.encode('utf-8')).hexdigest()
        if block_hash.startswith('0' * difficulty):  # Difficulty defines leading zeros
            return nonce, block_hash
        nonce += 1

def create_block(previous_hash):
    global pending_transactions
    nonce, block_hash = proof_of_work(previous_hash, pending_transactions)
    block = {
        "index": len(blockchain) + 1,
        "timestamp": time.time(),
        "transactions": pending_transactions,
        "previous_hash": previous_hash,
        "nonce": nonce,
        "hash": block_hash
    }
    pending_transactions = []  # Clear transactions after block creation
    return block

# Function to train a linear regression model on the Boston Housing data
def train_model():
    # Load the dataset
    data = pd.read_csv('/boston_housing_data.csv')
    
    # Preprocessing: target variable is 'medv'
    X = data.drop(columns=['medv'])  # Features
    y = data['medv']  # Target
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train the linear regression model
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # Return model coefficients and intercept
    result = {
        'coefficients': model.coef_.tolist(),
        'intercept': model.intercept_.tolist()
    }
    return result


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

    # Validation logic: Check if the result format is correct
    if isinstance(result['coefficients'], list) and isinstance(result['intercept'], (int, float)):
        
        # Additional validation of the coefficients and intercept (example range check)
        if not all(isinstance(coef, (int, float)) for coef in result['coefficients']):
            print("Invalid coefficient values received.")
            return jsonify({"status": "invalid", "error": "Invalid coefficients"}), 400
        
        if not (-1e6 < result['intercept'] < 1e6):
            print("Invalid intercept value received.")
            return jsonify({"status": "invalid", "error": "Invalid intercept"}), 400

        # Re-train the model locally to verify the received results
        print("Re-training the model locally for validation...")
        local_model = train_model()  # Function to train the model locally
        local_coefficients = local_model['coefficients']
        local_intercept = local_model['intercept']

        # Compare the locally generated model with the received results
        coefficients_match = all(
            abs(local_coef - received_coef) < 1e-5
            for local_coef, received_coef in zip(local_coefficients, result['coefficients'])
        )
        intercept_match = abs(local_intercept - result['intercept']) < 1e-5

        if not coefficients_match or not intercept_match:
            print("Mismatch between received results and locally generated results.")
            return jsonify({
                "status": "invalid",
                "error": "Mismatch between received and locally trained model."
            }), 400

        # Store the result with timestamp to track when the node received it
        pending_transactions.append({
            'result': result,
            'received_at': current_time,
            'broadcasted_at': broadcasted_at
        })
        
        print(f"\nNode received the result at {current_time}, broadcasted at {broadcasted_at}")

        # Check if this is the first result or validate based on your own conditions
        if len(pending_transactions) > 1:  # Create a block if multiple transactions are received
            # Create a block only if the result is valid
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

    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
