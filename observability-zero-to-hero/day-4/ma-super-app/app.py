from flask import Flask
from prometheus_client import Counter, Gauge, Histogram, generate_latest
import time, random, os

# ==== OpenTelemetry (Tracing) ====
from opentelemetry import trace, propagate
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor

# ---- Config OTel / Jaeger ----
SERVICE_NAME = os.getenv("OTEL_SERVICE_NAME", "super-app")
OTLP_TRACES_ENDPOINT = os.getenv(
    "OTEL_EXPORTER_OTLP_TRACES_ENDPOINT",
    # Par défaut pour Jaeger collector dans le ns "observability"
    "http://jaeger-collector.observability.svc.cluster.local:4318/v1/traces",
)

resource = Resource.create({"service.name": SERVICE_NAME})
provider = TracerProvider(resource=resource)
trace.set_tracer_provider(provider)

otlp_exporter = OTLPSpanExporter(endpoint=OTLP_TRACES_ENDPOINT, timeout=5)
provider.add_span_processor(BatchSpanProcessor(otlp_exporter))

# (Optionnel) B3/W3C propagators – W3C est activé par défaut
# propagate.set_global_textmap(TraceContextTextMapPropagator())  # déjà le default

app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)       # auto-instrumentation Flask
RequestsInstrumentor().instrument()           # traces des requêtes sortantes

# ======= Tes métriques Prometheus existantes =======
VISITES = Counter('visites_total', 'Nombre total de visites')
UTILISATEURS = Gauge('utilisateurs_actifs', 'Nombre d’utilisateurs actifs')
TEMPS = Histogram('temps_requete', 'Temps des requêtes')

@app.route("/")
def accueil():
    VISITES.inc()
    UTILISATEURS.set(random.randint(10, 100))
    with TEMPS.time():
        time.sleep(random.uniform(0.1, 0.5))
    # Crée un span manuel d’exemple
    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("business.compute"):
        time.sleep(random.uniform(0.05, 0.15))
    return "Bienvenue dans ma super app !"

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {'Content-Type': 'text/plain'}

@app.route("/crash")
def crash():
    os._exit(1)

if __name__ == "__main__":
    # 0.0.0.0 pour l’exposer dans le Pod
    app.run(host="0.0.0.0", port=5000)
