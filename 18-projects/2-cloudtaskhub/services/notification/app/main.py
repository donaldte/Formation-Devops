import json
import asyncio
from fastapi import FastAPI
from aiokafka import AIOKafkaConsumer
from tracing import setup_tracing
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.aiokafka import AIOKafkaInstrumentor
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(title="Analytics Service")

tracer = setup_tracing("notification-service")
FastAPIInstrumentor.instrument_app(app)
AIOKafkaInstrumentor().instrument()


fake_metrics = {
    "active_users": 12,
    "projects_created": 34,
    "billing_events": 0
}


async def consume_billing_events():
    consumer = AIOKafkaConsumer(
        "billing.events",
        bootstrap_servers="kafka:9092",
        group_id="analytics-group",
        value_deserializer=lambda v: json.loads(v.decode("utf-8"))
    )

    await consumer.start()
    try:
        async for msg in consumer:
            with tracer.start_as_current_span("process-notification"):
                fake_metrics["billing_events"] += 1
                print("📊 ANALYTICS UPDATED → ", fake_metrics)
    finally:
        await consumer.stop()


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(consume_billing_events())


@app.get("/metrics/app")
def app_metrics():
    return fake_metrics


@app.on_event("startup")
async def _startup():
    Instrumentator().instrument(app).expose(app)