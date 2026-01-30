FROM python:3.9-slim

# -------------------------
# System deps
# -------------------------
RUN apt-get update && apt-get install -y \
    wget \
    ca-certificates \
    bash \
    && rm -rf /var/lib/apt/lists/*

# -------------------------
# Install immudb (OFFICIAL DOC VERSION)
# -------------------------
RUN wget -q \
    https://github.com/vchain-us/immudb/releases/download/v1.9DOM.1/immudb-v1.9DOM.1-linux-amd64 \
    -O /usr/local/bin/immudb \
    && chmod +x /usr/local/bin/immudb

# -------------------------
# immudb dirs
# -------------------------
RUN mkdir -p /var/lib/immudb /app

# -------------------------
# Python app
# -------------------------
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# -------------------------
# Ports
# -------------------------
EXPOSE 8000 8080 3322

# -------------------------
# Start immudb + API
# -------------------------
CMD ["bash", "-c", "\
    immudb --dir=/var/lib/immudb --auth & \
    exec python main_api.py \
"]
