FROM python:3.10-slim

WORKDIR /app

# Upgrade pip
RUN pip install --upgrade pip

# Copy the requirements file first to leverage Docker cache
COPY requirements.txt .

# Install dependencies (no-cache to save space)
RUN pip install --no-cache-dir -r requirements.txt

# Copy all the rest of the application files
COPY . .

# Railway provides the PORT environment variable dynamically
ENV PORT=5000

# Start Gunicorn server
CMD gunicorn app:app --bind 0.0.0.0:${PORT:-5000} --timeout 120 --workers 1 --threads 2
