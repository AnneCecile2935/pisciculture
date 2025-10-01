FROM python:3.11-slim
WORKDIR /app

# Installe les dépendances système
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpq-dev \
	postgresql-client \
	netcat-openbsd\
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Met à jour pip
RUN python -m pip install --upgrade pip

# Crée un environnement virtuel
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copie les fichiers de dépendances
COPY app_pisci/requirements.txt /tmp/
COPY app_pisci/requirements-test.txt /tmp

# Installe les dépendances principales
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Installe les dépendances de test UNIQUEMENT si l'argument BUILD_FOR_TEST est "true"
ARG BUILD_FOR_TEST=false
RUN if [ "$BUILD_FOR_TEST" = "true" ]; then \
        pip install --no-cache-dir -r /tmp/requirements-test.txt; \
    fi

# Copie le reste de l'application
COPY app_pisci/ .

# Commande par défaut (pour le service "web")
# Optionnel : Attends que la base soit prête avant de lancer les migrations
CMD ["sh", "-c", "while ! nc -z db 5432; do sleep 1; done && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
