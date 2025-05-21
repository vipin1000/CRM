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
    netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Set the correct working directory
WORKDIR /app/CRM

# Create wait-for-db script
RUN echo '#!/bin/bash\n\
set -e\n\
\n\
host="$1"\n\
shift\n\
cmd="$@"\n\
\n\
until nc -z -v -w30 "$host" 3306\n\
do\n\
  echo "Waiting for database connection..."\n\
  sleep 5\n\
done\n\
\n\
echo "Database is up - executing command"\n\
exec $cmd' > /app/wait-for-db.sh && chmod +x /app/wait-for-db.sh

# Collect static files
RUN python manage.py collectstatic --noinput

# Run gunicorn with wait-for-db
CMD ["/bin/bash", "-c", "/app/wait-for-db.sh $MYSQLHOST python manage.py migrate && gunicorn CRM.wsgi:application --bind 0.0.0.0:$PORT"] 