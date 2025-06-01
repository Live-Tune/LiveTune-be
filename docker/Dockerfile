FROM --platform=linux/arm64 python:3.13.2-slim
RUN apt-get update && apt-get install -y build-essential
WORKDIR /app
COPY ../requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt
