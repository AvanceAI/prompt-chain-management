#!/bin/bash

IMAGE_NAME="prompt-chain-management"
CONTAINER_NAME="prompt-chain-management-test"

# Use the first argument as the directory where tests will be run, default to '/tests'
TEST_DIR=${1:-./}

# Define a cleanup function
cleanup() {
  echo "Cleaning up..."
  docker logs $CONTAINER_NAME  # Capture logs before stopping, in case of failure
  docker stop $CONTAINER_NAME || true
  docker rm $CONTAINER_NAME || true
  docker rmi $IMAGE_NAME || true
}

# Set the trap to call cleanup when the script exits
trap cleanup EXIT

# Build the Docker image
echo "Building Docker image..."
docker build -t $IMAGE_NAME . || { echo "Docker build failed"; exit 1; }

# Run the Docker container
echo "Starting Docker container..."
docker run --name $CONTAINER_NAME -d -p 8000:80 $IMAGE_NAME || { echo "Docker run failed"; exit 1; }

# Allow some time for the server to start
echo "Waiting for the server to start..."
sleep 1

# Execute the tests with pytest
echo "Running tests in directory: $TEST_DIR"
if ! docker exec $CONTAINER_NAME pytest -s $TEST_DIR; then
  echo "Tests failed. See error logs above."
  exit 1
fi

echo "Tests completed successfully."
