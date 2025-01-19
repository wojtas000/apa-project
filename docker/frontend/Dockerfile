# Use official Python image as a base
FROM python:3.10-slim

# Set the working directory
WORKDIR /frontend

# Copy the requirements.txt into the container
COPY ./docker/frontend/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the FastAPI application files into the container
COPY ./frontend .

# Expose the port the app will run on
EXPOSE 8501

# Command to run the FastAPI app
CMD ["streamlit", "run", "app.py"]
