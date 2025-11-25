what? 
kubernetes(deployment, service, pods, etc.)
appel Api (1000 requestes:  900 response succesfull, 100 response error)
logs(app , kubernetes, system, docker)(error, warning, info)
metrics (cpu, memory, network)
traces(request, response, latency)
request ---> load balancer ---> front end ---> app ---> database ---> backend ---> load balancer ---> response

dev/devops (monitoring, observability, logging, tracing, metrics)


l'observability est une approche d'ingenierie qui permet de garantir la disponibilité et la performance des applications.
why? 


how?

observability = monitoring + logging + tracing + metrics

monitoring = metrics + alerts(email, sms, slack, etc.) + dashboard (grafana, prometheus, etc.)

logging = logs + traces

dev/ops = observability ---> devops qui s'assure que les applications sont correctes et performantes

dev doit faire du logging(error, warning, info)