#!/bin/bash

# Define the service name as it appears in your docker-compose.yml file
SERVICE_NAME="prompt-chain-management"

# Use the first argument as the directory where tests will be run, default to './tests'
TEST_DIR=${1:-./tests}

# Define a cleanup function
cleanup() {
  echo "Cleaning up..."
  docker-compose logs $SERVICE_NAME  # Capture logs before stopping, in case of failure
  docker-compose stop $SERVICE_NAME
  docker-compose rm -f $SERVICE_NAME
  # docker-compose down would remove all services, networks, and volumes defined in docker-compose.yml
  # This line is commented out because it may not be the desired behavior if you have multiple services.
  # docker-compose down --rmi local
}

# Set the trap to call cleanup when the script exits
trap cleanup EXIT

# Build the Docker image and start the container with docker-compose
echo "Building and starting services with Docker Compose..."
docker-compose up -d --build $SERVICE_NAME || { echo "Docker Compose up failed"; exit 1; }

# Allow some time for the server to start
echo "Waiting for the server to start..."
sleep 5  # Adjust the sleep time if necessary

# Execute the tests with pytest
echo "Running tests in directory: $TEST_DIR"
if ! docker-compose exec $SERVICE_NAME pytest -s $TEST_DIR; then
  echo "Tests failed. See error logs above."
  exit 1
fi

echo "Tests completed successfully."

