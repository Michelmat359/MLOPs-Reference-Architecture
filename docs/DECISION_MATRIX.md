
# Matriz de decisión (resumen)

| Área | Alternativas | Criterios | Selección |
|---|---|---|---|
| Orquestador ML | Argo Workflows / Apache Airflow / Kubeflow Pipelines | Huella en K3s, integración K8s/S3, curva de aprendizaje, soporte GitOps | **Argo Workflows** |
| Registro y tracking | MLflow / Weights&Biases / Neptune | OSS, on-prem, facilidad de integración, auditoría | **MLflow** |
| Artefactos | MinIO / S3 nativo / Ceph RGW | On-prem, S3 compatible, facilidad | **MinIO** |
| Serving | FastAPI *custom* / Seldon Core / KServe | Simplicidad, requisitos mesh, ligereza | **FastAPI** (base) con opción de escalar a Seldon/KServe |
| Observabilidad | kube-prometheus-stack / VictoriaMetrics | Ecosistema, dashboards | **kube-prometheus-stack** |

**Riesgos & mitigaciones**  
- *Credenciales en valores por defecto*: usar Rancher Secrets/External Secrets y rotación.  
- *Hostnames/ingress*: si no hay DNS, usar `kubectl port-forward` desde Rancher.  
- *Peso del stack*: desactivar `loki` o `alertmanager` si el clúster es muy pequeño.  
