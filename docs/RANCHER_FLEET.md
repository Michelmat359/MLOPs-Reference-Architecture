
# Despliegue con Rancher Fleet

1. Entra en Rancher → **Cluster Explorer** → **Git Repos** → **Create**.
2. **Repository URL**: URL de tu fork (https://github.com/michelmat359/mlops-rancher-reference).
3. **Branch**: `main`. **Paths**: `fleet/bundle`.
4. Target: selecciona el/los clúster(es) y *namespace* de Fleet.
5. Agrega *Cluster Values* si quieres sobreescribir credenciales/hostnames:
   ```yaml
   helm:
     values:
       minio:
         auth:
           rootUser: "cambia"
           rootPassword: "cambia"
       mlflow:
         artifactStore:
           accessKey: "cambia"
           secretKey: "cambia"
         ingress:
           host: "mlflow.tu-dominio"
       argo-workflows:
         server:
           ingress:
             hosts: ["argo.tu-dominio"]
       kube-prometheus-stack:
         grafana:
           ingress:
             hosts: ["grafana.tu-dominio"]
   ```
6. **Create** → espera a que los *Releases* estén en `Deployed`.
