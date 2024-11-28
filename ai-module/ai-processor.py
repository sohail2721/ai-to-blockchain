import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import requests
import ipfshttpclient

# Connect to IPFS
ipfs_client = ipfshttpclient.connect('/dns/ipfs-node/tcp/5001/http')

# Fetch data from IPFS
data_hash = "QmdKyb6rV2ZUwPKAhubc8EzDHkKQLrmsEcHgLGmZEHgeeR"
data = ipfs_client.cat(data_hash).decode('utf-8')
df = pd.read_csv(data)

# Train linear regression model
X = df.drop('target', axis=1)
y = df['target']
model = LinearRegression().fit(X, y)

# Generate output (coefficients and intercept)
output = {"coefficients": model.coef_.tolist(), "intercept": model.intercept_}
print("AI Processing Output:", output)

# Save output for blockchain processing
with open("/shared-data/output.json", "w") as f:
    f.write(str(output))

