# Use a Python base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy Blockchain code and requirements.txt into the container
COPY blockchain.py /app/
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Command to run the blockchain node
CMD ["python", "blockchain.py"]
