FROM python:3.9-slim-buster

# Install system dependencies including curl and wget
RUN apt-get update && \
    apt-get install -y \
    build-essential \
    pkg-config \
    libmariadb-dev \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8085

CMD ["python", "rest.py"]
