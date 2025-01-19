# Base image from the official MLflow image
FROM ghcr.io/mlflow/mlflow:latest

# Install psycopg2 and other necessary dependencies
RUN pip install --no-cache-dir psycopg2-binary

# Expose the port the app will run on
EXPOSE 5000
