# Use a slim Python image
FROM python:3.11-slim

# Install system dependencies for Graphviz and PyGraphviz
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    graphviz \
    libgraphviz-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose Flask port
EXPOSE 5000

# Run the application
CMD  ["python", "-u", "-m", "flask", "-A", "datacompass", "run", "--host=0.0.0.0"]
