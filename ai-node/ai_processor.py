import requests
import time
import json
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from flask import Flask, request, jsonify



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
    
    success_nodes = []
    errors = []
    for node in nodes:
        try:
            # Use the container name to refer to the blockchain node (since they're on the same Docker network)
            blockchain_node_url = "http://blockchain-node:5002/validate_result"  # blockchain-node is the container name
            response = requests.post(blockchain_node_url, json=result)
            if response.status_code == 200:
                print(f"Node {node} accepted the result")
                success_nodes.append(node)
            else:
                errors.append(f"Error from node {node}: {response.status_code}")
        except requests.exceptions.RequestException as e:
            errors.append(f"Error broadcasting to node {node}: {e}")
    
    # Print successes and errors
    if success_nodes:
        print(f"Nodes that accepted the result: {', '.join(success_nodes)}")
    if errors:
        print(f"Errors: {', '.join(errors)}")

# Main function for training and broadcasting
def start_training():
    nodes = ["node-1", "node-2", "node-3"]  # List of all node addresses
    result = train_model()
    
    # Broadcast the result to other nodes for validation
    broadcast_result(result, nodes)

if __name__ == "__main__":
    start_training()
