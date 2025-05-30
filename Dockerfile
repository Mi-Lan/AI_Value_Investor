# Use Python 3.11 slim image for smaller size
FROM python:3.11-slim

# Install Chrome dependencies for headless mode
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY tikr_scraper/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the scraper code and static files
COPY tikr_scraper/ .

# Create outputs directory
RUN mkdir -p outputs

# Set proper permissions
RUN chmod -R 755 /app

# Run health check by default (can be overridden)
CMD ["python", "-c", "exec(open('/app/../health_check.py').read())"] 