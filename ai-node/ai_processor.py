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

def broadcast_result(result, nodes):
    print(f"Broadcasting result: {result}")  # Print the result being broadcasted
    
    first_broadcasted_node = None
    broadcast_time = None
    success_nodes = []
    errors = []

    for node in nodes:
        try:
            # Capture the current time as the broadcast time
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"Node {node} broadcasted the result at {timestamp}")

            # Send result to the node's validation endpoint
            response = requests.post(f"http://blockchain-node:5002/validate_result", json={'result': result, 'timestamp': timestamp})
            
            if response.status_code == 200:
                print(f"Node {node} accepted the result")
                if not first_broadcasted_node:  # Set the first broadcasted node
                    first_broadcasted_node = node
                    broadcast_time = timestamp
            else:
                errors.append(f"Error from node {node}: {response.status_code}")
        except requests.exceptions.RequestException as e:
            errors.append(f"Error broadcasting to node {node}: {e}")
    
    if first_broadcasted_node:
        print(f"The first node to broadcast the result is {first_broadcasted_node} at {broadcast_time}")
    if errors:
        print(f"Errors: {', '.join(errors)}")
    
    return first_broadcasted_node, broadcast_time

def start_training(training_cycles=5):
    nodes = ["node-1", "node-2", "node-3"]  # List of all node addresses
    
    for cycle in range(training_cycles):
        print(f"Starting training cycle {cycle + 1} of {training_cycles}...")
        
        # Train the model and get the result
        result = train_model()

        # Broadcast the result to other nodes for validation
        broadcast_result(result, nodes)

        # Optional: Wait for validation responses or some feedback from nodes
        # This is where you'd implement any logic to ensure that nodes have validated the result
        print(f"Waiting for validation from nodes for cycle {cycle + 1}...")
        time.sleep(5)  # Wait for 5 seconds, can be adjusted as needed

        # After waiting, you can choose to either repeat the training or end the cycle
        print(f"Training cycle {cycle + 1} completed.\n")
    
    print("Training process completed.")

if __name__ == "__main__":
    start_training()

# blockchain_node_url = "http://blockchain-node:5002/validate_result"  # blockchain-node is the container name