# Decentralized Machine Learning with IPFS and Blockchain

## Overview
This project integrates IPFS (InterPlanetary File System) with a blockchain-based system to enable decentralized machine learning. It allows multiple nodes to retrieve datasets from IPFS, train models, and validate results using blockchain mechanisms.

## Features
- **Decentralized Data Storage**: Uses IPFS to store and retrieve datasets securely.
- **Randomized Data Training**: Each training cycle operates on a randomly selected dataset partition.
- **Blockchain Integration**: Proof-of-work and consensus mechanisms verify training results.
- **Dockerized Environment**: Runs in isolated Docker containers for easy deployment.
- **Fault-Tolerant & Secure**: Ensures data integrity with IPFS hashing and cryptographic verification.

## System Architecture
1. **Data Upload**: The dataset is uploaded to IPFS, generating a unique CID (Content Identifier).
2. **Data Retrieval**: Each node retrieves the dataset from IPFS using the CID.
3. **Model Training**: Nodes train machine learning models on randomly selected partitions.
4. **Blockchain Verification**: Results are submitted to the blockchain for validation.
5. **Consensus Mechanism**: A proof-of-work algorithm ensures result integrity.

## Installation
### Prerequisites
- [IPFS](https://docs.ipfs.io/install/) (running on port `5002`)
- [Docker](https://docs.docker.com/get-docker/)
- Python 3.9+
- Required Python libraries: `pandas`, `scikit-learn`, `ipfshttpclient`, `flask`, `web3`

### Setup Instructions
1. Clone the repository:
   ```sh
   git clone https://github.com/your-repo/ipfs-ml-blockchain.git
   cd ipfs-ml-blockchain
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Start IPFS daemon (if not already running):
   ```sh
   ipfs daemon --init
   ```
4. Run the blockchain node:
   ```sh
   python blockchain_node.py
   ```
5. Start the training process:
   ```sh
   python ai_processor.py
   ```

## Usage
### Upload Dataset to IPFS
```sh
ipfs add boston_housing_data.csv
```
Copy the CID returned and update `ai_processor.py` to fetch the file using IPFS.

### Train Model
Run the training script:
```sh
python ai_processor.py
```
This fetches the dataset, trains the model on a random partition, and submits the results for verification.

### Check IPFS File Availability
Verify dataset availability on IPFS:
```sh
ipfs cat <CID>
```

### Check Blockchain Logs
Inspect blockchain logs for validation:
```sh
tail -f blockchain.log
```

## Troubleshooting
### IPFS Connection Error
If you encounter `Connection refused` errors, check:
- IPFS daemon is running on port `5002`
- Use `lsof -i -P -n | grep LISTEN` to verify port usage
- Restart IPFS: `ipfs daemon`

### Docker Issues
If using Docker:
```sh
docker-compose up --build
```

## Future Enhancements
- Implement federated learning with privacy-preserving techniques.
- Improve consensus mechanism for scalable verification.
- Add support for multiple ML models.

## License
This project is licensed under the MIT License.
