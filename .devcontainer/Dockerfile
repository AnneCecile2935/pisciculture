FROM mcr.microsoft.com/devcontainers/python:1-3.12-bullseye

# Installe Docker CLI et Docker Compose
RUN apt-get update && \
    apt-get install -y docker.io && \
    curl -fsSL https://get.docker.com | sh && \
    pip install docker-compose
