#!/usr/bin/env bash
set -euo pipefail

# Add required Helm repositories
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo add seldonio https://storage.googleapis.com/seldon-charts
helm repo update

# Build dependencies for subcharts (to vendor .tgz in each charts/ dir)
helm dependency update charts/monitoring
helm dependency update charts/redis-edge
helm dependency update charts/redis-cloud
helm dependency update charts/seldon-operator

echo "Dependencies vendored. Commit the generated 'charts/*/charts/*.tgz' and 'Chart.lock' files."
