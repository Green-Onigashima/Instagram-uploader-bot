# Use official Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements.txt to the container
COPY requirements.txt .

# Upgrade pip to the latest version
RUN pip install --upgrade pip

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose port and run the application (replace this line based on your app)
CMD ["python", "app.py"]
