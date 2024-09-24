#!/bin/bash

# ==============================================================================
# Installation Script for Python Project
# ==============================================================================
# This script automates the setup of a Python project in a virtual environment.
#
# Instructions to use this script:
# 1. Make sure this script has executable permissions:
#    chmod +x install.sh
#
# 2. Run the script using the following command:
#    ./install.sh
#
# 3. The script will create a virtual environment, activate it, and install the
#    required dependencies listed in the requirements.txt file.
#
# 4. After running the script, remember to:
#    - Activate the virtual environment before working on the project:
#      source venv/bin/activate
#
#    - Deactivate the virtual environment when you're done:
#      deactivate
# ==============================================================================

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
echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt

# Check if dependencies were installed successfully
if [ $? -ne 0 ]; then
    echo "Failed to install dependencies."
    deactivate
    exit 1
fi

# Success message with a hint about activation and deactivation
echo "Setup completed successfully!"
echo ""
echo "To start using the environment, activate it with the following command:"
echo "source venv/bin/activate"
echo ""
echo "When you're done, deactivate the environment by running:"
echo "deactivate"
