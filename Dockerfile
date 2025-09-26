FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpq-dev \
	postgresql-client \
	netcat-openbsd\
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN python -m pip install --upgrade pip
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Change /workspace en /app ici :

COPY app_pisci/requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt
COPY app_pisci/ .

# Optionnel : Attends que la base soit prête avant de lancer les migrations
CMD ["sh", "-c", "while ! nc -z db 5432; do sleep 1; done && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
