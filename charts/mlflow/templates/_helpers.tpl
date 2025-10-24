
{{- define "mlflow.name" -}}
mlflow
{{- end -}}

{{- define "mlflow.fullname" -}}
{{ printf "%s-%s" .Release.Name (include "mlflow.name" .) }}
{{- end -}}
