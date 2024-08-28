# Use a Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the src directory into the container
COPY src/ /app/src/

# Set the environment variable for Flask
ENV FLASK_APP=src/app.py
ENV FLASK_ENV=development
ENV AWS_ACCESS_KEY_ID=""
ENV AWS_SECRET_ACCESS_KEY=""
ENV AWS_SESSION_TOKEN=""

ENV AWS_DEFAULT_REGION=us-east-1

# Expose the port Flask runs on
EXPOSE 5000

# Run the application
CMD ["python", "src/app.py"]
