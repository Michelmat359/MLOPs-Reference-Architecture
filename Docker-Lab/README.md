
# Industrial MLOps Laboratory 🏭🤖

A complete, containerized End-to-End Industrial AI environment. This project simulates a factory floor, connects it via MQTT to an Edge AI environment, and manages the model lifecycle using MLflow and MinIO (S3).

## 🏗 Architecture

The stack consists of 3 main planes:
1.  **OT Plane (Operational Technology):**
    * **Node-RED:** Simulates industrial machinery (PLC) and acts as the HMI (Human-Machine Interface).
    * **Mosquitto:** MQTT Broker for standard industrial communication.
2.  **IT Plane (Data Science):**
    * **Jupyter Lab:** The environment for coding, training, and running the "Edge AI" inference script.
    * **Python Stack:** Includes `paho-mqtt` for connectivity and `scikit-learn` for AI.
3.  **Governance Plane (MLOps):**
    * **MLflow:** Tracks experiments and registers versioned models.
    * **MinIO:** S3-compatible object storage for model artifacts.
    * **Postgres:** Backend database for MLflow metadata.

---

## 🚀 Deployment Guide

### Prerequisites
* **Docker Desktop** installed and running.
* **macOS Users:** Ensure AirPlay Receiver is disabled (System Settings -> General -> AirDrop & Handoff -> AirPlay Receiver: **OFF**) to free up port `5000`.

### 1. Installation
Clone the repository (or navigate to your folder) and build the stack:

```bash
# Build images and start containers in detached mode
docker-compose up --build -d

```

### 2. Accessing the Services

| Service | URL | Credentials | Description |
| --- | --- | --- | --- |
| **Jupyter Lab** | `http://localhost:8888` | (See logs*) | Python IDE & Edge Runner |
| **MLflow UI** | `http://localhost:5000` | N/A | Model Registry & Tracking |
| **Node-RED** | `http://localhost:1880` | N/A | Flow Editor (Simulator) |
| **Dashboard** | `http://localhost:1880/ui` | N/A | Operator Control Panel |
| **MinIO Console** | `http://localhost:9001` | `admin` / `password123` | S3 Storage Browser |

*> To get the Jupyter Token the first time:*

```bash
docker logs ind-jupyter-lab 2>&1 | grep "token="

```

---

## 🧪 How to Run the Experiment

### Step 1: Train the Model (The "Cold" Phase)

1. Open **Jupyter Lab**.
2. Navigate to the `work/` directory (IMPORTANT: Files outside `work/` are not saved).
3. Create a new Notebook and run the **Training Script**.
* *Goal:* Generate synthetic data, train a RandomForest, and log it to MLflow.
* *Verification:* Check `http://localhost:5000` to see the new Experiment and Run ID.



### Step 2: Configure the Plant (Node-RED)

1. Open **Node-RED** (`http://localhost:1880`).
2. **Input:** Create an `mqtt in` node subscribed to `planta/sensores`.
3. **Output:** Create an `mqtt in` node subscribed to `planta/prediccion`.
4. **Dashboard:** Connect `Gauge` and `Text` nodes to the output to visualize the results.
5. Click **Deploy**.

### Step 3: Run Real-Time Inference (The "Hot" Phase)

1. In Jupyter, copy the **Run ID** from MLflow.
2. Update the **Inference Script** with your specific `RUN_ID`.
3. Execute the script.
* It will load the model from MinIO.
* It will connect to the Broker.
* It will start listening to simulated sensor data.


4. Open the **Dashboard** (`http://localhost:1880/ui`).
5. Watch the gauges move and the AI Status change between **OPTIMAL 🟢** and **DANGER 🔴** automatically.

---

## 🛑 Stopping the Lab

To stop the environment and free up resources:

```bash
docker-compose down

```
