#!/bin/bash

# (⊕) GAFJ E2E Test Rig - Pip/Venv Edition
# This script tests a fresh installation using standard pip and venv.

set -e # Exit immediately if a command exits with a non-zero status.

echo "--- 🚀 Starting Pip/Venv E2E Test ---"

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
echo "--- 🧪 Simulating a fresh user install with pip/venv ---"

# 1. Create a new virtual environment
python3 -m venv .venv

# 2. Activate it (for the shell session in the script)
source .venv/bin/activate

# (⊕) Ensure pip is up-to-date within the venv
python -m pip install --upgrade pip

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the script in file-out mode
# We pipe a simple string to it to test the stdin reading.
echo "Ahoy there, matey!" | python main.py

# 5. Check if the output file was created
# We just check if the 'out' directory is not empty
echo "Ahoy there, matey!" | python main.py --save
if [ -z "$(ls -A out)" ]; then
  echo "--- ❌ TEST FAILED: No output file was created! ---"
  exit 1
fi

echo "--- ✅ TEST PASSED: Pip/Venv installation successful and output file created! ---"

exit 0
