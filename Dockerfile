FROM python:3.11-slim

# Set environment variables for a clean, writable Rust install location
ENV DEBIAN_FRONTEND=noninteractive
ENV RUSTUP_HOME=/usr/local/rustup
ENV CARGO_HOME=/usr/local/cargo
ENV PATH=$CARGO_HOME/bin:$PATH

# Install system build deps
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       curl \
       ca-certificates \
       git \
       gcc \
       g++ \
       libssl-dev \
       pkg-config \
       libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Rust toolchain non-interactively into /usr/local (writable in container)
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y --no-modify-path \
    && /bin/sh -c "source /usr/local/cargo/env || true"

# Copy requirements first to leverage Docker layer cache
WORKDIR /app
COPY requirements.txt /app/requirements.txt

# Upgrade pip and install Python deps (maturin/cargo builds will use the Rust toolchain above)
RUN python -m pip install --upgrade pip setuptools wheel \
    && pip install -r requirements.txt

# Copy application code
COPY . /app

EXPOSE 8080

# Use Gunicorn with Uvicorn worker for FastAPI
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "main:app", "--bind", "0.0.0.0:8080", "--workers", "1"]
