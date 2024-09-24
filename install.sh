#!/bin/bash

# Check if Python3 is installed
if ! command -v python3 &> /dev/null
then
    echo "Python3 is not installed. Please install Python3 and try again."
    exit
fi

# Create a virtual environment
echo "Creating a virtual environment..."
python3 -m venv venv

# Check if the virtual environment was created successfully
if [ $? -ne 0 ]; then
    echo "Failed to create a virtual environment."
    exit 1
fi

# Activate the virtual environment
echo "Activating the virtual environment..."
source venv/bin/activate

# Check if the virtual environment is activated
if [ $? -ne 0 ]; then
    echo "Failed to activate the virtual environment."
    exit 1
fi

# Install required dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Check if dependencies were installed successfully
if [ $? -ne 0 ]; then
    echo "Failed to install dependencies."
    deactivate
    exit 1
fi

echo "Setup completed successfully."
