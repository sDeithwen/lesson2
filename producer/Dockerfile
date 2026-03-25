FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN pip install flask

EXPOSE 5000

COPY producer.py .

CMD ["python", "producer.py"]