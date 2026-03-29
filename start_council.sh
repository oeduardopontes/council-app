#!/bin/bash

# Add Homebrew to PATH
eval "$(/opt/homebrew/bin/brew shellenv)"

# Change to app directory
cd /Users/dwardo/council-app

# Load environment variables from .env
set -a
source .env
set +a

# Activate virtual environment
source venv/bin/activate

# Start gunicorn
exec gunicorn -w 4 -b 0.0.0.0:8080 --access-logfile /Users/dwardo/council-app/access.log --error-logfile /Users/dwardo/council-app/error.log app:app
