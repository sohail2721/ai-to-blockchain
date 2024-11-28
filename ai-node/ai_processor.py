import requests
import time
import json
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# Function to train a linear regression model on the Boston Housing data
def train_model():
    # Load the dataset
    data = pd.read_csv('/app/boston_housing_data.csv')
    
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

# Function to broadcast the result to other nodes
def broadcast_result(result, nodes):
    for node in nodes:
        try:
            response = requests.post(f"http://{node}/validate_result", json=result)
            if response.status_code == 200:
                print(f"Node {node} accepted the result")
        except requests.exceptions.RequestException as e:
            print(f"Error broadcasting to node {node}: {e}")

# Main function for training and broadcasting
def start_training():
    nodes = ["node-1", "node-2", "node-3"]  # List of all node addresses
    result = train_model()
    
    # Broadcast the result to other nodes for validation
    broadcast_result(result, nodes)

    # Repeat the process (mining/training again)
    time.sleep(5)
    start_training()

if __name__ == "__main__":
    start_training()
