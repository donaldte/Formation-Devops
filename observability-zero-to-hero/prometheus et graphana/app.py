from flask import Flask
from prometheus_client import start_http_server, Counter

app = Flask(__name__)
counter = Counter('flask_request_count', 'Nombre de requêtes')

@app.route('/')
def hello():
    counter.inc()
    return "Hello, Flask!"

if __name__ == '__main__':
    start_http_server(8000)  # métriques Prometheus
    app.run(host='0.0.0.0', port=5000)