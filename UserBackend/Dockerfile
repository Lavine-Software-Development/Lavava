# Use the official Python image from the Docker Hub with the slim variant for smaller size
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install build essentials and clean up in one RUN command to reduce image size
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Make port 5553 available to the world outside this container
EXPOSE 5001
EXPOSE 5002

# Run the application
CMD ["python", "app.py"]