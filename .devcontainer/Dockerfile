FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpq-dev \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN python -m pip install --upgrade pip
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Change /workspace en /app ici :
WORKDIR /app
COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt
COPY . /app  

EXPOSE 8000
