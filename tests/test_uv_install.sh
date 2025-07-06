#!/bin/bash

# (⊕) GAFJ E2E Test Rig - UV Edition
# This script tests a fresh installation using uv.

set -e # Exit immediately if a command exits with a non-zero status.

echo "--- 🚀 Starting UV E2E Test ---"

# Create a temporary directory for a clean-room test
TEST_DIR=$(mktemp -d)

# Function to clean up on exit
cleanup() {
  echo "--- 🧹 Cleaning up test directory: $TEST_DIR ---"
  rm -rf "$TEST_DIR"
}
trap cleanup EXIT

# Copy project files to the test directory
echo "--- 📂 Copying project files to temp directory ---"
cp main.py requirements.txt "$TEST_DIR"
cd "$TEST_DIR"
mkdir out

# --- The Test --- 
echo "--- 🧪 Simulating a fresh user install with uv ---"

# 1. Create a new virtual environment
if ! command -v uv &> /dev/null
then
    echo "UV could not be found, skipping test."
    exit 0
fi
uv venv

# 2. Activate it (for the shell session in the script)
source .venv/bin/activate

# 3. Install dependencies
uv pip install -r requirements.txt

# 4. Run the script in file-out mode
# We pipe a simple string to it to test the stdin reading.
echo "Ahoy there, matey!" | python main.py

# 5. Check if the output file was created
# We just check if the 'out' directory is not empty
if [ -z "$(ls -A out)" ]; then
  echo "--- ❌ TEST FAILED: No output file was created! ---"
  exit 1
fi

echo "--- ✅ TEST PASSED: UV installation successful and output file created! ---"

exit 0