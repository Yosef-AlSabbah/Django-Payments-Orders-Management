FROM ubuntu:latest
# Use an official Python runtime as a parent image
FROM python:3.12.2-slim-bullseye

# Set the working directory in the container
WORKDIR /app

# Install system dependencies (if needed for some libraries, like psycopg2)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at /app
COPY . /app/

# Install the Python dependencies from requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Set environment variables for Django settings (adjust as needed)
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=myshop.settings

# Collect static files (optional if you're using static files in production)
# RUN python manage.py collectstatic --noinput

# Apply database migrations (optional, especially useful for first-time setup)
RUN python manage.py migrate

# Expose the port Django will run on
EXPOSE 8080

ENV PORT=8080

# Start the Django development server (you can replace this with a more production-ready option like Gunicorn)
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]
CMD gunicorn myshop.wsgi:application --bind 0.0.0.0:"${PORT}"

ENTRYPOINT ["top", "-b"]