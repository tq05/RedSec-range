{{/* Common labels for all resources in a range. */}}
{{- define "redsec.labels" -}}
app.kubernetes.io/managed-by: {{ .Release.Service }}
app.kubernetes.io/part-of: redsec-range
redsec.io/range: {{ .Values.range.module | quote }}
redsec.io/slug: {{ .Values.range.slug | quote }}
{{- end -}}

{{- define "redsec.dropHost" -}}
http://{{ .Values.drop.name }}.{{ .Values.range.namespace }}.svc.cluster.local:{{ .Values.drop.port }}
{{- end -}}
