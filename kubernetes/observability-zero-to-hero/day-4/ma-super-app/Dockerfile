# -------- Base --------
FROM python:3.10-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 1) Installer les deps en root (plus simple/fiable)
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# 2) Créer l’utilisateur non-root ensuite
RUN adduser --disabled-password --gecos "" appuser
USER appuser

# 3) Copier le code après (cache-friendly)
COPY --chown=appuser:appuser . .

# 4) Env OTel (tu peux aussi les définir dans le Deployment)
ENV OTEL_SERVICE_NAME=flask-demo \
    OTEL_TRACES_EXPORTER=otlp \
    OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf \
    OTEL_EXPORTER_OTLP_TRACES_ENDPOINT=http://jaeger-collector.observability.svc.cluster.local:4318/v1/traces \
    OTEL_TRACES_SAMPLER=always_on

EXPOSE 5000

CMD ["python", "app.py"]
