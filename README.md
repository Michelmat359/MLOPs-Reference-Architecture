
# MLOps Reference Stack for Rancher/K3s

> **Objetivo**: despliegue *one-click* (vía **Rancher/Fleet** o **Helm**) de una **arquitectura base de MLOps** lista para usar en industria 4.0/5.0: *tracking y registro de modelos (MLflow) + artefactos S3 (MinIO) + orquestación de pipelines (Argo Workflows) + observabilidad (Prometheus/Grafana + Loki) + ejemplo de *training* y *serving**.

La selección de servicios, la separación por dominios (*system/dev/prod*) y los flujos CI/CD/CT siguen las mejores prácticas sintetizadas en el artículo entregado por el autor (ciclo de vida completo, observabilidad, edge–cloud, registros y trazabilidad).

## Arquitectura (visión lógica)

```mermaid
flowchart LR
  subgraph System["mlops-system (plataforma)"]
    A[MinIO (S3)] <--S3--> B[MLflow Tracking/Registry]
    C[(PostgreSQL)]
    B --> C
    D[Argo Workflows + UI]
    E[Prometheus]
    F[Grafana]
    G[Loki + Promtail]
    E --> F
    G --> F
  end

  subgraph Dev["mlops-dev (entrenamiento)"]
    H[Argo: DAG Entrenar/Evaluar/Registrar]
    H -->|artefactos| A
    H -->|metrics| E
    H -->|run| B
  end

  subgraph Prod["mlops-prod (serving)"]
    I[API FastAPI modelo v1]
    I -->|logs| G
    I -->|metrics| E
    I <-->|carga modelo| A
    B -->|URI de Modelo| I
  end

  D <-->|DAGs| H
  F -->|dashboards| Users[Operaciones & Data/OT]
```

### Componentes

- **MinIO**: almacén S3 para artefactos y *datasets*.
- **PostgreSQL**: *backend-store* para MLflow.
- **MLflow**: *tracking + registry* de experimentos y modelos.
- **Argo Workflows**: orquestación nativa Kubernetes para *pipelines* de ML y **CronWorkflows** (entrenos/reentrenos y chequeos de *drift*).
- **Prometheus + Grafana + Loki**: métricas, *dashboards* y logs (*observabilidad* de plataforma + modelos).
- **FastAPI Model Server (ejemplo)**: *serving* canarizado de modelos registrados en MLflow.


## Despliegue con Rancher (Fleet)

1. **Añadir este repositorio** en Rancher → *Cluster Explorer* → **Git Repos** (Fleet) → *Create*.
2. Selecciona el/los clúster(es) destino y apunta a la carpeta `fleet/bundle`.
3. Personaliza dominios/credenciales en `fleet/bundle/fleet.yaml` o usa *Cluster values* en Fleet.
4. Pulsa **Deploy**. Fleet instalará:
   - Namespaces: `mlops-system`, `mlops-dev`, `mlops-prod`
   - MinIO, PostgreSQL, MLflow, Argo Workflows, kube-prometheus-stack, Loki
   - Ingress (Traefik) para UIs: `mlflow.<tu-dominio>`, `minio.<tu-dominio>`, `grafana.<tu-dominio>`, `argo.<tu-dominio>`

> Si no tienes DNS, puedes usar *port-forward* desde Rancher para acceder a las UIs.

## Despliegue con Helm (alternativa CLI)

```bash
# 1) Namespaces
kubectl apply -f k8s/namespaces.yaml

# 2) Repos
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo add argo https://argoproj.github.io/argo-helm
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update

# 3) MinIO + PostgreSQL + Prometheus/Grafana + Argo
helm upgrade --install minio bitnami/minio -n mlops-system -f helm-values/minio.yaml
helm upgrade --install pg bitnami/postgresql -n mlops-system -f helm-values/postgresql.yaml
helm upgrade --install monitoring prometheus-community/kube-prometheus-stack -n mlops-system -f helm-values/kube-prometheus-stack.yaml
helm upgrade --install loki grafana/loki-stack -n mlops-system -f helm-values/loki-stack.yaml
helm upgrade --install argo argo/argo-workflows -n mlops-system -f helm-values/argo-workflows.yaml

# 4) MLflow (chart local)
helm upgrade --install mlflow charts/mlflow -n mlops-system -f helm-values/mlflow.yaml
```

## Accesos por defecto (¡cámbialos!)

- MinIO (console): usuario `mlops`, contraseña `mlops123` (ver `helm-values/minio.yaml`).
- PostgreSQL: usuario/db `mlflow` (ver `helm-values/postgresql.yaml`).
- MLflow: expone `http://mlflow.<tu-dominio>` (token opcional).

> **Importante**: rota todas las credenciales en *producción* y usa *Secrets* de Kubernetes o gestores externos (Vault/ESO).

## Ejemplo de *pipeline* (Argo)

- `workflows/train-register.yaml` entrena un modelo de clasificación con **scikit-learn**, registra el *run* y sube artefactos a MinIO/MLflow.
- `workflows/drift-cron.yaml` calcula métricas de *drift* con **Evidently** y las publica en Prometheus.

```bash
# Ejecutar pipeline de ejemplo
kubectl -n mlops-dev apply -f workflows/train-register.yaml

# Programar chequeo de drift (cada hora)
kubectl -n mlops-dev apply -f workflows/drift-cron.yaml
```

## *Serving* de un modelo (FastAPI)

- Construye/push la imagen `images/serving-fastapi/` a tu registry.
- Despliega el Helm chart `charts/fastapi-model-server` apuntando a la URI del modelo en MLflow (por ejemplo `models:/demo-model/Production`).

```bash
helm upgrade --install demo charts/fastapi-model-server -n mlops-prod -f helm-values/fastapi-model-server.yaml
```

## Seguridad y cumplimiento

- Tráfico TLS con `cert-manager` (opcional), autenticación básica en UIs, *NetworkPolicies* de ejemplo (`k8s/networkpolicies.yaml`).
- *Dashboards* en Grafana para **SLI/SLO** del modelo y de plataforma.
- Registros y *rollbacks* desde **MLflow Registry** + *blue/green* en el *serving* de ejemplo.

---

**Referencias/encaje**: esta arquitectura implementa el ciclo de vida, la gobernanza, el registro de modelos y la observabilidad que se describen como claves para llevar ML a producción en la industria 4.0/5.0 (MLOps end-to-end, *edge–cloud*, CI/CD/CT, *drift* y *human-in-the-loop*).
