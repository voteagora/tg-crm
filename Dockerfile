FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Install pre-built TDLib
RUN wget -q https://github.com/tdlib/td/releases/download/v1.8.0/libtdjson_1.8.0_amd64.deb && \
    dpkg -i libtdjson_1.8.0_amd64.deb || true && \
    apt-get -f install -y && \
    rm libtdjson_1.8.0_amd64.deb

# Set up app directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Run the application
CMD uvicorn src.main:app --host 0.0.0.0 --port $PORT
