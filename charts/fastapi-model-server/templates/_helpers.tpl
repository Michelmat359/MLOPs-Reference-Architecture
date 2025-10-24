
{{- define "srv.name" -}} fastapi-model-server {{- end -}}
{{- define "srv.fullname" -}} {{ printf "%s-%s" .Release.Name (include "srv.name" .) }} {{- end -}}
