# -------------------------------------------------
# Base: pinned, reproducible Python 3.9
# -------------------------------------------------
FROM python@sha256:c65dadac8789fed40962578392e99a0528dcb868442c75d144e68ba858984837

WORKDIR /app

# -------------------------------------------------
# System dependencies
# -------------------------------------------------
RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    bash \
    && rm -rf /var/lib/apt/lists/*

# -------------------------------------------------
# Install immudb (PINNED VERSION)
# -------------------------------------------------
ENV IMMUDB_VERSION=1.10.0

RUN curl -L \
    https://github.com/codenotary/immudb/releases/download/v${IMMUDB_VERSION}/immudb-linux-amd64 \
    -o /usr/local/bin/immudb \
    && chmod +x /usr/local/bin/immudb

# -------------------------------------------------
# App setup
# -------------------------------------------------
RUN mkdir -p /app/data
RUN mkdir -p /var/lib/immudb

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Render only needs the HTTP port
EXPOSE 8000

# -------------------------------------------------
# Start immudb + backend
# -------------------------------------------------
CMD ["bash", "-c", "\
    immudb server --auth & \
    sleep 2 && \
    python main_api.py \
"]
