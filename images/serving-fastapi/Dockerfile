
FROM python:3.10-slim

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1     PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py /app/app.py

EXPOSE 8080
ENTRYPOINT ["python", "/app/app.py"]
