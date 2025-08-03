from flask import Flask
from prometheus_client import Counter, Gauge, Histogram, generate_latest
import time, random, os

app = Flask(__name__)

# Capteur pour compter les visites
VISITES = Counter('visites_total', 'Nombre total de visites')
# Capteur pour mesurer les utilisateurs
UTILISATEURS = Gauge('utilisateurs_actifs', 'Nombre d’utilisateurs actifs')
# Capteur pour mesurer le temps
TEMPS = Histogram('temps_requete', 'Temps des requêtes')

@app.route("/")
def accueil():
    VISITES.inc()  # Compte +1 visite
    UTILISATEURS.set(random.randint(10, 100))  # Simule des utilisateurs
    with TEMPS.time():
        time.sleep(random.uniform(0.1, 0.5))  # Simule un petit délai
    return "Bienvenue dans ma super app !"

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {'Content-Type': 'text/plain'}

@app.route("/crash")
def crash():
    os._exit(1)  # Simule un problème

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)