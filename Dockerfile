FROM python:3.9-slim

# Install system dependencies and TDLib
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    gperf \
    libssl-dev \
    zlib1g-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install TDLib from source with optimized build
RUN cd /tmp && \
    git clone -b v1.8.0 --single-branch --depth 1 https://github.com/tdlib/td.git && \
    cd td && \
    mkdir build && \
    cd build && \
    cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX:PATH=/usr/local .. && \
    cmake --build . --target install -j$(nproc) && \
    cd / && \
    rm -rf /tmp/td

# Set up app directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Run the application
CMD uvicorn src.main:app --host 0.0.0.0 --port $PORT
