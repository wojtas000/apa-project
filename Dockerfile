# Use official Python image as a base
FROM python:3.10-slim

# Set the working directory
WORKDIR /apa-ml

# Copy flair models into the container
COPY ./ml-models/flair ./ml-models/flair

# Copy the requirements.txt into the container
COPY requirements.in .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.in

# Copy the FastAPI application files into the container
COPY ./app .

# Expose the port the app will run on
EXPOSE 8000

# Command to run the FastAPI app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
