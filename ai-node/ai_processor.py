import requests
import time
import json
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from flask import Flask, request, jsonify
from datetime import datetime



app = Flask(__name__)

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

import random
from datetime import datetime
import requests
import hashlib


def proof_of_work(previous_hash, transactions, difficulty=4):
    nonce = 0
    while True:
        block_string = f"{previous_hash}{transactions}{nonce}"
        block_hash = hashlib.sha256(block_string.encode('utf-8')).hexdigest()
        if block_hash.startswith('0' * difficulty):  # Difficulty defines leading zeros
            return nonce, block_hash
        nonce += 1

def validate_pow(previous_hash, transactions, nonce, difficulty=4):
    block_string = f"{previous_hash}{transactions}{nonce}"
    block_hash = hashlib.sha256(block_string.encode('utf-8')).hexdigest()
    return block_hash.startswith('0' * difficulty)

def broadcast_result(result, nodes, blockchain):
    first_broadcasted_node = None
    broadcast_time = None

    # Capture the current blockchain state
    previous_hash = blockchain[-1]['hash'] if blockchain else '0'
    
    # Perform PoW
    nonce, block_hash = proof_of_work(previous_hash, [result])
    print(f"Broadcasting block with hash: {block_hash} and nonce: {nonce}")
    
    for node in nodes:
        try:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            response = requests.post(
                f"http://blockchain-node:5002/validate_result",
                json={
                    'result': result,
                    'timestamp': timestamp,
                    'previous_hash': previous_hash,
                    'nonce': nonce,
                    'hash': block_hash
                }
            )
            if response.status_code == 200:
                print(f"Node {node} validated the result")
                if not first_broadcasted_node:
                    first_broadcasted_node = node
                    broadcast_time = timestamp
        except Exception as e:
            print(f"Error broadcasting to node {node}: {e}")
    
    return first_broadcasted_node, broadcast_time



def start_training(training_cycles=5):
    nodes = ["node-1", "node-2", "node-3"]  # List of all node addresses
    blockchain = []  # Initialize blockchain
    
    for cycle in range(training_cycles):
        print(f"Starting training cycle {cycle + 1} of {training_cycles}...")
        
        # Train the model and get the result
        result = train_model()

        # Broadcast the result to other nodes for validation
        broadcast_result(result, nodes, blockchain)

        # Optional: Wait for validation responses or some feedback from nodes
        print(f"Waiting for validation from nodes for cycle {cycle + 1}...")
        time.sleep(5)  # Wait for 5 seconds, can be adjusted as needed

        # After waiting, you can choose to either repeat the training or end the cycle
        print(f"Training cycle {cycle + 1} completed.\n")
    
    print("Training process completed.")


if __name__ == "__main__":
    start_training()

# blockchain_node_url = "http://blockchain-node:5002/validate_result"  # blockchain-node is the container name