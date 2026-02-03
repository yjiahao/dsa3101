# Use Python Alpine base image
FROM python:3.11-alpine

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
COPY templates /app/templates
COPY static /app/static
COPY avatar3.py .

# Install dependencies needed for many Python packages to build on Alpine
RUN apk add --no-cache build-base libffi-dev
RUN pip install --upgrade pip 
RUN pip install -r requirements.txt

# Command to run the app
CMD ["flask", "-A", "avatar3", "run", "-h", "0.0.0.0", "-p", "5000"]
