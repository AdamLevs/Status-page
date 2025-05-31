#!/bin/bash

# Load env if needed (optional)
if [ ! -f .env ]; then
  echo ".env file not found!"
  exit 1
fi

# Start application
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
