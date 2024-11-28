# Use a Python base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy AI processor code and requirements.txt into the container
COPY ai_processor.py /app/
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Command to run the AI model
CMD ["python", "ai_processor.py"]
