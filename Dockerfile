# Use a specific version of the Python base image
FROM python:3.8.12-slim-buster AS base

# Set environment variable
ENV FLASK_APP application.py

# Install required packages
RUN apt-get update && \
    apt-get install -y \
        poppler-utils \
        tesseract-ocr \
        qpdf \
        ghostscript && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create a dedicated directory for the application
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

# Use a smaller base image for the final image
FROM python:3.8.12-slim-buster
COPY --from=base / /

# Copy the rest of the application
COPY . .

# Set the working directory for the container
WORKDIR /app

# Set the command to run when the container starts
CMD ["flask", "run"]

# Check the health of the container
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl --fail http://localhost:5000/ || exit 1