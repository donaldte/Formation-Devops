import json
from fastapi import FastAPI
from pydantic import BaseModel
from aiokafka import AIOKafkaProducer
import json

from tracing import setup_tracing
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.aiokafka import AIOKafkaInstrumentor
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(title="Billing Service")

tracer = setup_tracing("billing-service")

FastAPIInstrumentor.instrument_app(app)
AIOKafkaInstrumentor().instrument()

producer = None


@app.on_event("startup")
async def startup_event():
    global producer
    producer = AIOKafkaProducer(
        bootstrap_servers="kafka:9092",
        value_serializer=lambda v: json.dumps(v).encode("utf-8")
    )
    await producer.start()


@app.on_event("shutdown")
async def shutdown_event():
    global producer
    if producer:
        await producer.stop()


class BillingEvent(BaseModel):
    user_email: str
    plan_name: str
    status: str


@app.post("/webhook")
async def webhook(event: BillingEvent):
    with tracer.start_as_current_span("produce-billing-event"):
        await producer.send_and_wait(
            "billing.events",
            {
                "email": event.user_email,
                "plan": event.plan_name,
                "status": event.status
            }
        )
    return {"message": "billing event produced to kafka"}


@app.on_event("startup")
async def _startup():
    Instrumentator().instrument(app).expose(app)