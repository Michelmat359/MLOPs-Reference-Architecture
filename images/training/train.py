
import os, time
import mlflow
import mlflow.sklearn
import numpy as np
import pandas as pd
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score

TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://mlflow-mlflow.mlops-system.svc.cluster.local:5000")
EXPERIMENT = os.getenv("MLFLOW_EXPERIMENT", "demo-experiment")
MODEL_NAME = os.getenv("MODEL_NAME", "demo-model")
RANDOM_SEED = int(os.getenv("RANDOM_SEED", "42"))

mlflow.set_tracking_uri(TRACKING_URI)
mlflow.set_experiment(EXPERIMENT)

def main():
    # synthetic dataset (deterministic)
    X, y = make_classification(n_samples=5000, n_features=20, n_informative=8, n_redundant=4,
                               n_clusters_per_class=2, weights=[0.6, 0.4], class_sep=1.2,
                               random_state=RANDOM_SEED)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=RANDOM_SEED)

    with mlflow.start_run(run_name=f"train-{int(time.time())}") as run:
        params = {"C": 1.0, "max_iter": 200, "solver": "lbfgs", "random_state": RANDOM_SEED}
        mlflow.log_params(params)

        model = LogisticRegression(**params)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        acc = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        mlflow.log_metrics({"accuracy": acc, "f1": f1})

        mlflow.sklearn.log_model(model, artifact_path="model")
        # Registrar en el Registry
        result = mlflow.register_model(
            f"runs:/{run.info.run_id}/model",
            MODEL_NAME
        )
        print(f"Registered model: {result.name} v{result.version}")

if __name__ == "__main__":
    main()
