# -------- Base --------
FROM python:3.10-slim

WORKDIR /app

# Evite les .pyc, force un flush stdout
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# (Optionnel mais utile) utilisateur non-root
RUN adduser --disabled-password --gecos "" appuser
USER appuser

# Copie des sources en dernier pour optimiser le cache si tu passes à un requirements.txt
COPY --chown=appuser:appuser . .

# Déps runtime
# - Flask + Prometheus
# - OpenTelemetry SDK + Exporter OTLP + auto-instrumentations Flask/Requests
RUN pip install --no-cache-dir \
    flask==3.0.3 \
    prometheus_client==0.20.0 \
    opentelemetry-api==1.27.0 \
    opentelemetry-sdk==1.27.0 \
    opentelemetry-exporter-otlp==1.27.0 \
    opentelemetry-instrumentation==0.48b0 \
    opentelemetry-instrumentation-flask==0.48b0 \
    opentelemetry-instrumentation-requests==0.48b0

# ----- OpenTelemetry vers Jaeger (OTLP/HTTP) -----
# Tu peux override ces variables dans le Deployment
ENV OTEL_SERVICE_NAME=flask-demo \
    OTEL_TRACES_EXPORTER=otlp \
    OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf \
    OTEL_EXPORTER_OTLP_TRACES_ENDPOINT=http://jaeger-collector.observability.svc.cluster.local:4318/v1/traces \
    OTEL_TRACES_SAMPLER=always_on

EXPOSE 5000

CMD ["python", "app.py"]
