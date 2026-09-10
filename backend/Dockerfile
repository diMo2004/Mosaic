# Use official lightweight Python image
FROM python:3.13-slim

# Prevent Python from writing pyc files and buffering stdout and stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV HOME=/app

# Set work directory
WORKDIR /app

# Install system dependencies for psycopg2 and media handling
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY backend/requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy backend application files
COPY backend/ /app/

# Create media and static root directories and non-root user
RUN mkdir -p /app/staticfiles /app/media && \
    adduser --disabled-password --no-create-home appuser && \
    chown -R appuser:appuser /app

USER appuser

# Expose Render default port
EXPOSE 8000

# Entrypoint to run migrations, collectstatic, and start gunicorn
CMD ["sh", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn config.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 2 --threads 2"]