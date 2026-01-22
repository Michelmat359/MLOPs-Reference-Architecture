FROM jupyter/scipy-notebook:latest
LABEL authors="miguelangel"

# Cambiamos a usuario root para instalar dependencias de sistema si hiciera falta
USER root

# Instalamos librerías del stack industrial
# NOTA: paho-mqtt es lo que usarás para hablar con Node-RED vía MQTT
RUN pip install \
    mlflow==2.7.1 \
    boto3 \
    psycopg2-binary \
    paho-mqtt \
    alibi-detect \
    evidently \
    minio

# Volvemos al usuario estandar de Jupyter para evitar problemas de permisos
USER ${NB_UID}