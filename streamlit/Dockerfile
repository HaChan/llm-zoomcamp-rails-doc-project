FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN python -m pip install --upgrade pip
RUN pip install --default-timeout=100 --retries=5 --no-cache-dir -r requirements.txt
