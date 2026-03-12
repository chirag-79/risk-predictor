# Use Python 3.10 official image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements
COPY backend/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire project
COPY . .

# Train model on startup (this is run once)
RUN cd /app && python backend/model.py

# Run FastAPI on port 8000
CMD ["uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "8000"]
