
# IndMLOps-Lab: Reference Architecture for Industrial MLOps 🏭🤖

**IndMLOps-Lab** is a containerized Reference Implementation of a Hybrid Industrial MLOps Architecture. It is designed to bridge the gap between **Operational Technology (OT)** and **Information Technology (IT)**, providing a complete environment to simulate, develop, and govern Machine Learning lifecycles in manufacturing settings.

## 📖 Overview

This laboratory simulates a "smart factory" environment where sensor data is generated at the edge, processed for model training in a central core, and deployed back to the edge for real-time inference, all under strict governance and observability.

### Architecture Planes
The stack is organized into three logical planes, following the ISA-95 model principles:

1.  **OT Plane (The Factory Floor):**
    * **Node-RED:** Simulates industrial machinery (PLCs), sensors, and acts as the Human-Machine Interface (HMI).
    * **Mosquitto:** MQTT Broker for low-latency, standard industrial telemetry.
    * **Edge Inference:** Simulates runtime environments for model execution close to the data source.

2.  **IT Plane (The Core/Server):**
    * **MLflow:** Centralized Model Registry and Experiment Tracking.
    * **MinIO:** S3-compatible Object Storage (On-Premise) for Data Sovereignty.
    * **PostgreSQL:** Metadata backend for the registry.
    * **Jupyter Lab:** Data Science Integrated Development Environment (IDE).

3.  **Governance Plane (Observability):**
    * **Prometheus:** Scrapes technical metrics (system health, latency, drift).
    * **Grafana:** Visualizes business KPIs and model performance dashboards.

---

# Kubernetes Deployment Guide ☸️

This guide details the deployment of the **IndMLOps** architecture on a Kubernetes cluster. Unlike the flat network of Docker Compose, this setup simulates a production environment using **Namespaces** for logical isolation and **Persistent Volumes (PV)** for data durability.

## ✅ Prerequisites

* **Kubernetes Cluster** active (Docker Desktop K8s, Minikube, K3s, or Cloud).
* **kubectl** CLI tool installed and configured.

## 📂 Deployment Structure

The manifests are organized by layer order:
* `00-namespaces.yaml`: Defines `it-core`, `ot-edge`, and `governance`.
* `01-storage/`: Defines Persistent Volume Claims (PVCs).
* `02-it-core/`: Core services (MLflow, MinIO, DB).
* `03-ot-edge/`: Edge services (Node-RED, MQTT).
* `04-governance/`: Monitoring services (Prometheus, Grafana).

## 1. Installation Steps

Run the following commands from the `k8s-manifests/` directory:

### Phase 1: Infrastructure
Initialize namespaces and storage.

```bash
kubectl apply -f 00-namespaces.yaml
kubectl apply -f 01-storage/

```

### Phase 2: Application Layers

Deploy the services.

```bash
# Deploy IT Core (The Brain)
kubectl apply -f 02-it-core/

# Deploy OT Edge (The Factory)
kubectl apply -f 03-ot-edge/

# Deploy Governance (The Eyes)
kubectl apply -f 04-governance/

```

*Wait 1-2 minutes for pods to initialize.* Verify status:

```bash
kubectl get pods -A

```

## 2. Accessing Services (Port Forwarding)

In Kubernetes, services are isolated by default. To access them from `localhost`, use `port-forward` in **separate terminal tabs**:

**1. MinIO Console (S3 Storage)**

```bash
kubectl port-forward svc/minio-svc -n it-core 9001:9001
# URL: http://localhost:9001 (User: admin / Pass: password123)

```

**2. MLflow UI (Registry)**

```bash
kubectl port-forward svc/mlflow-svc -n it-core 5000:5000
# URL: http://localhost:5000

```

**3. Node-RED (Factory Sim)**

```bash
kubectl port-forward svc/nodered-svc -n ot-edge 1880:1880
# URL: http://localhost:1880

```

**4. Grafana (Dashboards)**

```bash
kubectl port-forward svc/grafana-svc -n governance 3000:3000
# URL: http://localhost:3000 (User: admin / Pass: admin)

```

## ⚙️ Initial Configuration (Mandatory)

Because this is a fresh persistence layer, you must initialize the storage bucket manually:

1. Log in to **MinIO** (`http://localhost:9001`).
2. Click **Create Bucket**.
3. Name it: `mlflow-bucket`.
* *Note: Without this step, MLflow training scripts will fail when trying to upload artifacts.*



## 🗑️ Cleanup

To remove the entire deployment and namespaces:

```bash
kubectl delete namespace it-core ot-edge governance

```
