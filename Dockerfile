FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies (optional but good practice)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency file and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY app/ app/

# Expose port 8000 for FastAPI
EXPOSE 8000

# Default command to run the app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
