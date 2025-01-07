#!/bin/bash

# Variables
PACKAGE_NAME="caddkit"
PACKAGE_PATH="dist/caddkit-0.1.0.dev0-py3-none-any.whl"

echo "Starting package reinstallation..."

# Step 1: Uninstall the package
echo "Uninstalling $PACKAGE_NAME..."
pip uninstall -y "$PACKAGE_NAME"
if [ $? -ne 0 ]; then
    echo "Error: Failed to uninstall $PACKAGE_NAME. Exiting."
    exit 1
fi

# Step 2: Build the package
echo "Building the package..."
python setup.py bdist_wheel
if [ $? -ne 0 ]; then
    echo "Error: Failed to build the package. Exiting."
    exit 1
fi

# Step 3: Install the package
echo "Installing $PACKAGE_NAME from $PACKAGE_PATH..."
pip install "$PACKAGE_PATH"
if [ $? -ne 0 ]; then
    echo "Error: Failed to install $PACKAGE_NAME. Exiting."
    exit 1
fi

echo "$PACKAGE_NAME reinstalled successfully!"
