# Use official Python image as a base
FROM python:3.10-slim

# Set the working directory
WORKDIR /backend

# Copy the requirements.txt into the container
COPY ./docker/backend/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install system dependencies (like git) AFTER pip install
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy scripts into the container
COPY ./scripts ./scripts

# Copy the app code into the container
COPY ./app ./app

# Expose the port the app will run on
EXPOSE 8000

# Command to run the FastAPI app
CMD ["sh", "-c", "python -m scripts.start_worker & uvicorn app.main:app --host 0.0.0.0 --port 8000"]

