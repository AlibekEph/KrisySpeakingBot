# Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
COPY settings.ini .
COPY app ./app
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "-u", "app/main.py"]
