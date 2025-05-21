FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Set the correct working directory
WORKDIR /app/CRM

# Debug: List directory contents
RUN ls -la

# Debug: Check Python path
RUN which python

# Debug: Check if manage.py exists
RUN test -f manage.py && echo "manage.py exists" || echo "manage.py not found"

# Collect static files
RUN python manage.py collectstatic --noinput

# Run gunicorn
CMD gunicorn CRM.wsgi:application --bind 0.0.0.0:$PORT 