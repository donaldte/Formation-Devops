from fastapi import FastAPI
from pydantic import BaseModel
import httpx
from tracing import setup_tracing
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(title="Gateway Service")

# Setup tracing
tracer = setup_tracing("gateway-service")

FastAPIInstrumentor.instrument_app(app)
HTTPXClientInstrumentor().instrument()


SERVICES = {
    "auth": "http://auth-service:8000",
    "project": "http://project-service:8001",
    "billing": "http://billing-service:8002",
    "notification": "http://notification-service:8003",
    "analytics": "http://analytics-service:8004",
}


@app.get("/health")
def health():
    return {"status": "ok", "service": "gateway"}


@app.get("/status")
async def status():
    results = {}
    async with httpx.AsyncClient() as client:
        for name, url in SERVICES.items():
            try:
                r = await client.get(f"{url}/health", timeout=2.0)
                results[name] = r.json()
            except Exception as e:
                results[name] = {"status": "down", "error": str(e)}
    return results


# ----------- WORKFLOW SECTION ------------
class WorkflowRequest(BaseModel):
    email: str
    password: str
    project_title: str


@app.post("/workflow/create-project")
async def workflow_create_project(data: WorkflowRequest):
    with tracer.start_as_current_span("workflow-create-project"):
        async with httpx.AsyncClient() as client:

            with tracer.start_as_current_span("register-user"):
                r1 = await client.post(
                    f"{SERVICES['auth']}/register",
                    json={"email": data.email, "password": data.password}
                )

            with tracer.start_as_current_span("create-project"):
                r2 = await client.post(
                    f"{SERVICES['project']}/tasks",
                    json={"id": 999, "title": data.project_title, "done": False}
                )

            with tracer.start_as_current_span("billing-event"):
                r3 = await client.post(
                    f"{SERVICES['billing']}/webhook",
                    json={
                        "user_email": data.email,
                        "plan_name": "Free",
                        "status": "success",
                    }
                )

            with tracer.start_as_current_span("send-notification"):
                r4 = await client.post(
                    f"{SERVICES['notification']}/send",
                    json={
                        "to": data.email,
                        "subject": "Votre projet est créé",
                        "body": f"Le projet '{data.project_title}' a bien été créé."
                    }
                )

            with tracer.start_as_current_span("get-analytics"):
                r5 = await client.get(f"{SERVICES['analytics']}/metrics/app")

    return {
        "workflow": "completed",
        "steps": {
            "auth": r1.json(),
            "project": r2.json(),
            "billing": r3.json(),
            "notification": r4.json(),
            "analytics": r5.json(),
        },
    }
    
    
@app.on_event("startup")
async def _startup():
    Instrumentator().instrument(app).expose(app)    
