from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry import trace


def setup_tracing(service_name: str):
    resource = Resource(attributes={"service.name": service_name})

    provider = TracerProvider(resource=resource)
    exporter = OTLPSpanExporter(endpoint="http://jaeger:4318/v1/traces")

    processor = BatchSpanProcessor(exporter)
    provider.add_span_processor(processor)

    trace.set_tracer_provider(provider)

    return trace.get_tracer(service_name)
