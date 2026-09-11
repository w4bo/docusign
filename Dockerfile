FROM python:3.12-slim

WORKDIR /app

# Install dependencies first (layer cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code and config
COPY main.py config.yaml ./

# tosign/ and signed/ are mounted as volumes; create them so the image works standalone too.
RUN mkdir -p tosign signed

# signature.png and PDFs are provided at runtime via docker-compose volumes.
# No COPY needed here.

CMD ["python", "main.py"]
