# Use an official lightweight Python image
FROM python:3.11-slim

# Set a working directory inside the container
WORKDIR /app

# Copy a Python script into the container
COPY hello.py .

# Run the script when the container starts
ENTRYPOINT ["/app/entrypoint.sh"]

# hello:latest