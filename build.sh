#!/bin/bash
# Build script for Render deployment

echo "Installing Python dependencies..."
pip install -r backend/requirements.txt

echo "Training ML model..."
cd backend
python model.py
cd ..

echo "Build complete!"
