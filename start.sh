#!/bin/bash

# Set default port if not provided
if [ -z "$PORT" ] || [ "$PORT" = "\$PORT" ]; then
    export PORT=8000
    echo "Setting PORT to default: $PORT"
fi

echo "Starting application on port: $PORT"
python main.py
