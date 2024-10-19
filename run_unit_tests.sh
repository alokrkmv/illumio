#!/bin/bash

# Exit script immediately if any command fails
set -e

# Install pytest if it's not installed
if ! python -c "import pytest" &> /dev/null; then
    echo "Installing pytest..."
    pip install pytest
else
    echo "pytest is already installed."
fi

TEST_SUITE_1="unit_tests/test_helper.py"
TEST_SUITE_2="unit_tests/test_log_processor.py"


# Run pytest on the first test suite
echo "Running helper test suite.........."
pytest "$TEST_SUITE_1"

# Run pytest on the second test suite
echo "Running log processor test suites.........."
pytest "$TEST_SUITE_2"

echo "All tests executed successfully!"
