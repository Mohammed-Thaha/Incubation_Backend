# Use official Python image
FROM python:3.12-slim

# Install PostgreSQL client libs (only needed for psycopg2, not psycopg2-binary)
# RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the event_calendar package
COPY ./event_calendar /app/event_calendar

# Expose port
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "event_calendar.main:app", "--host", "0.0.0.0", "--port", "8000"]
