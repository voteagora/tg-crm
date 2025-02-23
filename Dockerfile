FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    gperf \
    git \
    zlib1g-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Clone and build TDLib
RUN git clone https://github.com/tdlib/td.git && \
    cd td && \
    mkdir build && \
    cd build && \
    cmake -DCMAKE_BUILD_TYPE=Release .. && \
    cmake --build . && \
    make install && \
    cd ../.. && \
    rm -rf td

# Set up app directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Run the application
CMD uvicorn src.main:app --host 0.0.0.0 --port $PORT
