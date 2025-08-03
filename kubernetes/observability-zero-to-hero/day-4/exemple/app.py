# app.py

# Importation de Flask pour créer une application web simple
from flask import Flask

# Importation des types de métriques depuis la bibliothèque Prometheus
from prometheus_client import Counter, Gauge, Histogram, Summary, generate_latest

# Bibliothèques standards pour simuler des délais et générer des valeurs aléatoires
import time, random, os

# Création de l’application Flask
app = Flask(__name__)

# ------------------- 🔢 MÉTRIQUES PROMETHEUS -------------------

# 1. Counter : Compteur qui ne peut qu’augmenter
# Sert ici à compter le nombre total de requêtes HTTP reçues sur la page d’accueil
REQUEST_COUNTER = Counter('http_requests_total', 'Nombre total de requêtes HTTP')

# 2. Gauge : Valeur qui peut monter ou descendre
# Exemple ici : nombre d’utilisateurs actifs (valeur simulée)
ACTIVE_USERS = Gauge('active_users', 'Utilisateurs actifs')

# 3. Histogram : Mesure la durée de requêtes dans des intervalles (buckets)
# Permet de voir par exemple combien de requêtes ont duré moins de 0.1s, entre 0.1s et 0.5s, etc.
REQUEST_DURATION = Histogram('request_duration_seconds', 'Durée des requêtes')

# 4. Summary : Fournit des statistiques avancées (comme les percentiles) sur les latences
REQUEST_LATENCY = Summary('request_latency_seconds', 'Résumé des latences')

# ------------------- 🌐 ROUTES -------------------

@app.route("/")
def home():
    """
    Page d’accueil : cette route déclenche les différentes métriques
    """

    # Incrémente le compteur de requêtes
    REQUEST_COUNTER.inc()

    # Définit un nombre aléatoire d’utilisateurs actifs entre 10 et 100
    ACTIVE_USERS.set(random.randint(10, 100))

    # Mesure automatiquement le temps que prend le bloc ci-dessous
    with REQUEST_DURATION.time():
        # Simule un traitement aléatoire entre 0.1 et 0.5 secondes
        time.sleep(random.uniform(0.1, 0.5))

    # Enregistre manuellement une latence simulée entre 0.1 et 0.5 secondes
    REQUEST_LATENCY.observe(random.uniform(0.1, 0.5))

    return "Bienvenue dans l’app instrumentée Flask"

@app.route("/metrics")
def metrics():
    """
    Endpoint obligatoire pour Prometheus : il collecte les métriques à cet emplacement
    Retourne toutes les métriques actuelles au format texte compatible Prometheus
    """
    return generate_latest(), 200, {'Content-Type': 'text/plain'}

@app.route("/crash")
def crash():
    """
    Endpoint pour simuler un crash de l’application
    Utilisé pour tester les alertes avec Alertmanager
    """
    os._exit(1)  # Ferme brutalement le processus (simule un plantage)
