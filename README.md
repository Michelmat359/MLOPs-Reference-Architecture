# 🧩 MLOPS Reference Architecture (Edge–Cloud Industrial Environment)

This repository provides a **Reference Architecture for MLOps in Industrial Engineering (MLOps-IE-RA)**, designed as a **reproducible and modular environment** deployable via **Helm, Rancher, and K3s**.  
It enables the **deployment, monitoring, and evaluation** of machine learning pipelines across **Edge–Hybrid–Cloud** configurations.

---

## 📘 Overview

MLOps-IE-RA is an open, declarative **GitOps-ready experimental framework** to study the deployment, operation, and monitoring of AI services in **Industry 4.0 / 5.0** environments.  
It represents the infrastructure layer of the **MLOps-IE-RA architecture**, proposed for empirical validation of MLOps strategies aligned with **RAMI 4.0** and **ISA-95** standards.

The environment is designed to:

- Support **heterogeneous Edge–Cloud deployments** (e.g., Raspberry Pi 4 + industrial node).
- Enable **continuous experimentation** (monitoring, load-testing, retraining loops).
- Provide **observable, reproducible, and automatable** pipelines.
- Quantify MLOps performance through **operational metrics** (P95 latency, MTTR, DORA indicators).

---

## 🏗️ Components and Services

Each functional block is implemented as a **Helm Chart** located in `charts/`:

| Chart | Namespace | Description |
|-------|------------|-------------|
| `monitoring` | `monitoring` | Deploys **Prometheus + Grafana** stack for metrics collection, dashboards and ServiceMonitors. |
| `redis-edge` | `mlops-edge` | Lightweight **Redis** instance (Bitnami) pinned to the **Edge node** (Raspberry Pi 4, arm64). |
| `redis-cloud` | `mlops-cloud` | Redis instance for **core/cloud** node (amd64). |
| `fastapi-edge` | `mlops-edge` | FastAPI-based **model serving microservice**, exposing `/predict`, `/health`, `/metrics`. |
| `k6-loadtest` | `monitoring` or `mlops-edge` | Executes **load-testing** with Grafana k6, generating throughput and latency metrics. |
| `seldon-operator` | `seldon-system` | (Optional) Deploys **Seldon Core Operator** for managed model deployments. |

All components are defined declaratively as Helm releases, supporting **GitOps automation** through Rancher or GitLab CI/CD.

---

## 🧰 System Requirements

| Layer | Requirement |
|--------|-------------|
| **Cluster** | K3s ≥ v1.28 (tested on v1.28.5 +k3s1) |
| **Orchestrator** | Rancher (v2.8 +) managing a K3s cluster |
| **Nodes** | At least 1 core node (amd64) + 1 edge node (arm64 e.g., Raspberry Pi 4 8 GB) |
| **Storage** | `local-path` StorageClass or equivalent CSI driver |
| **Ingress** | Traefik (default in K3s) |
| **Network** | Internal connectivity between edge ↔ core nodes (IPv4/IPv6 supported) |
| **Helm** | v3.13 + configured in Rancher |
| **Optional** | MetalLB (for LoadBalancer services), cert-manager (for HTTPS ingress) |

---

## 🪜 Installation Steps (Rancher + GitLab GitOps)

### 1. Add Git Repository to Rancher

1. In *Apps & Marketplace → Repositories → Create Repository*  
   - **Type:** Git  
   - **URL:** `https://gitlab.com/<your-user>/MLOPS-Reference-Architecture.git`  
   - **Branch:** `main`

2. Rancher automatically fetches all sub-charts under `charts/`.

---

### 2. Create Required Namespaces

Before deploying, ensure the following namespaces exist:

```bash
kubectl create ns monitoring
kubectl create ns mlops-edge
kubectl create ns mlops-cloud
kubectl create ns seldon-system   # optional
```

3) Desplegar con Rancher

Instala los charts individualmente:

Ruta del chart	Namespace	Notas
charts/monitoring	monitoring	Prometheus + Grafana
charts/redis-edge	mlops-edge	Redis Edge
charts/redis-cloud	mlops-cloud	Redis Cloud
charts/fastapi-edge	mlops-edge	Serving del modelo
charts/k6-loadtest	monitoring	Carga
(opcional) charts/seldon-operator	seldon-system	Operador

Como umbrella (si lo usas):

helm install mlopsra ./ --namespace=mlops --create-namespace --wait --timeout=10m
MLOPS-Reference-Architecture/
├── charts/
│   ├── fastapi-edge/
│   ├── k6-loadtest/
│   ├── monitoring/
│   ├── redis-edge/
│   ├── redis-cloud/
│   └── seldon-operator/
├── environments/
│   ├── edge/
│   └── cloud/
├── Chart.yaml
├── values.yaml
└── README.md


🔍 Validación y monitorización

Grafana: paneles de latencia (P50/P95/P99), throughput, ratio de error, DORA.

Prometheus: http_request_duration_seconds_bucket, http_requests_total; con Seldon: inference_latency_seconds_bucket.

Pruebas de carga (k6): RPS, tasa de éxito, latencia media.

Edge: temperatura (exporter RPi), CPU/RAM.

📊 Escenarios experimentales
Topología	Serving	Reentrenos	Feature Store	Notas
Edge-Only	RPi 4 (arm64)	Manual	Redis Edge	Mínima latencia
Híbrido	RPi 4 + Cloud	Nodo cloud	Redis Edge + Cloud	Equilibrado
Cloud-Only	Nodo x86	Cloud	Redis Cloud	Cómputo centralizado
🔬 Contexto científico

Este entorno acompaña al artículo:

“Machine Learning Operations in Industrial Engineering: Enabling Reliable Decision-Making in Industry 4.0 and 5.0” (Mateo-Casali et al., 2025)

Implementa el marco MLOps-IE-RA para evaluar arquitecturas Edge–Cloud en contextos industriales.

