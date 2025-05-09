#!/bin/bash

# Exit if any command fails
set -e

# Run site generation
python3 src/main.py

# Change to public directory and start server
cd public
echo "Serving site at http://localhost:8888"
python3 -m http.server 8888
