FROM python:3.11-slim

WORKDIR /app

# Copy project files
COPY . /app

# Install dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Mount the volume at /data
VOLUME /data

# Set the entry point to scheduler.py
CMD ["python3", "scheduler.py"]
