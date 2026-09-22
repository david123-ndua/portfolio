FROM python:3.12-slim

# Prevent Python from creating .pyc files
# and make logs appear immediately
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Application directory
WORKDIR /app

# Install dependencies first
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Make sure required directories exist
RUN mkdir -p instance static/uploads

# Flask application port
EXPOSE 5000

# Start Flask
CMD ["python", "app.py"]