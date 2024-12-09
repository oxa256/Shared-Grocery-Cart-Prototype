# Use an official Python base image
FROM python:3.11-slim

# Set working directory in the container
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy your application code
COPY skeleton /app/skeleton

# Set the default command to run your app
CMD ["python", "/app/skeleton/your_main_script.py"]
