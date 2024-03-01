FROM python:3.11-slim

# Env variables
ENV PYTHONUNBUFFERED=1 \
    PORT=8007

WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
 && pip install poetry

# Copy only the necessary files for cronjob
COPY poetry.lock pyproject.toml /app/
RUN poetry config virtualenvs.create false \
 && poetry install --no-dev --no-interaction --no-ansi

# Copy service from repo to docker container
COPY app/services /app/app/services

# Run cron job
CMD ["python", "app/services/auto_predict_service.py"]
