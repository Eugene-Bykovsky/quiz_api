FROM python:3.11-slim

WORKDIR /app

COPY ./requirements.txt .

RUN apt-get update && apt-get install -y nano && pip3 install --upgrade pip && pip3 install -r ./requirements.txt --no-cache-dir

COPY app.py .

