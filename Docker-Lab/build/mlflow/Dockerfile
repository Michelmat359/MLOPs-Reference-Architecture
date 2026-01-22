FROM python:3.9-slim
LABEL authors="miguelangel"
# Instalamos MLflow y los conectores necesarios para MinIO (boto3) y Postgres (psycopg2)
RUN pip install mlflow==2.7.1 boto3 psycopg2-binary

# El comando por defecto al arrancar
CMD ["mlflow", "server", \
     "--host", "0.0.0.0", \
     "--port", "5000", \
     "--backend-store-uri", "postgresql://mlflow:mlflowpassword@postgres:5432/mlflow_db", \
     "--default-artifact-root", "s3://mlflow-bucket/"]