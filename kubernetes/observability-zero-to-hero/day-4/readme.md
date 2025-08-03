

## 🎛️ **Instrumentation**

### 📌 Définition :

L’**instrumentation** désigne le processus consistant à **ajouter des capacités de surveillance (monitoring)** à vos applications, systèmes ou services.

Cela implique :

* d’intégrer du **code** ou
* d’utiliser des **outils spécialisés** pour **collecter des métriques, des journaux (logs) ou des traces**, fournissant ainsi une **vue claire sur les performances et le comportement du système.**

---

## 🎯 **Objectifs de l’instrumentation**

| Objectif                     | Description                                                                           |
| ---------------------------- | ------------------------------------------------------------------------------------- |
| 👀 **Visibilité**            | Obtenir une visibilité sur l’état interne de l’application ou de l’infrastructure     |
| 📊 **Collecte de métriques** | Mesurer des indicateurs clés comme l’usage CPU, la mémoire, les requêtes, les erreurs |
| 🛠 **Débogage**              | Diagnostiquer rapidement les problèmes grâce à des données précises                   |

---

## ⚙️ **Comment fonctionne l’instrumentation ?**

* 🎯 **Instrumentation au niveau du code** :
  Cela consiste à **ajouter des instructions dans le code de votre application** pour exposer des métriques personnalisées.

Exemple : 


## 🧰 📦 **Bibliothèques d’instrumentation Prometheus selon le langage**

> Pour exposer des métriques personnalisées dans une application, Prometheus propose des **clients officiels ou communautaires** pour différents langages.

| Langage         | Bibliothèque recommandée                                                        | Description rapide                                          |
| --------------- | ------------------------------------------------------------------------------- | ----------------------------------------------------------- |
| **Node.js**     | [`prom-client`](https://github.com/siimon/prom-client)                          | Bibliothèque officielle pour créer et exposer des métriques |
| **Python**      | [`prometheus_client`](https://github.com/prometheus/client_python)              | Supporte Counter, Gauge, Histogram, Summary                 |
| **Go (Golang)** | [`prometheus/client_golang`](https://github.com/prometheus/client_golang)       | Client officiel complet, utilisé par les exporters          |
| **Java**        | [`simpleclient`](https://github.com/prometheus/client_java)                     | Intégration avec Spring Boot, Micrometer, etc.              |
| **Ruby**        | [`prometheus/client_ruby`](https://github.com/prometheus/client_ruby)           | Facile à intégrer dans Rails/Sinatra                        |
| **.NET / C#**   | [`prometheus-net`](https://github.com/prometheus-net/prometheus-net)            | Pour ASP.NET Core, support natif                            |
| **Rust**        | [`prometheus`](https://github.com/tikv/rust-prometheus)                         | Utilisé dans les systèmes haute performance                 |
| **PHP**         | [`jimdo/prometheus_client_php`](https://github.com/Jimdo/prometheus_client_php) | Client communautaire pour PHP                               |

---

## 🧩 🎯 **Intégration par framework**

> Certains frameworks populaires proposent une **intégration prête à l’emploi** pour faciliter l’exposition des métriques :

| Framework              | Intégration / Package dédié                                                                                  | Exemple de métrique exposée                 |
| ---------------------- | ------------------------------------------------------------------------------------------------------------ | ------------------------------------------- |
| **Express (Node.js)**  | [`express-prometheus-middleware`](https://www.npmjs.com/package/express-prometheus-middleware)               | Temps de réponse, erreurs, requêtes         |
| **Flask (Python)**     | [`prometheus_flask_exporter`](https://github.com/rycus86/prometheus_flask_exporter)                          | Exportation automatique de `/metrics`       |
| **Django (Python)**    | [`django-prometheus`](https://github.com/korfuri/django-prometheus)                                          | ORM, middleware, requêtes HTTP, modèles     |
| **Spring Boot (Java)** | via [`Micrometer`](https://micrometer.io/) + Actuator                                                        | Intégré avec Prometheus + Grafana           |
| **ASP.NET Core**       | Intégration avec [`prometheus-net.AspNetCore`](https://github.com/prometheus-net/prometheus-net#aspnet-core) | Compteurs, usage mémoire, temps d’exécution |
| **FastAPI (Python)**   | [`prometheus-fastapi-instrumentator`](https://github.com/trallnag/prometheus-fastapi-instrumentator)         | Temps de réponse, taux d’erreur, routes     |

---

### 📝 Exemple concret :

> 🔍 **Exemple avec Node.js** :

```javascript
const client = require('prom-client');

const httpRequests = new client.Counter({
  name: 'http_requests_total',
  help: 'Nombre total de requêtes HTTP',
});

httpRequests.inc(); // +1 requête
```

> 🔍 **Exemple avec Flask (Python)** :

```python
from prometheus_client import Counter

http_requests = Counter('http_requests_total', 'Nombre total de requêtes HTTP')
http_requests.inc()
```


## 📈 **L’instrumentation avec Prometheus**

### 🧲 Prometheus récupère les métriques via des **exporters** :

| Exporter                   | Utilité                                                         |
| -------------------------- | --------------------------------------------------------------- |
| 🖥 **Node Exporter**       | Collecte les métriques système (CPU, RAM…) sur un serveur Linux |
| 🛢 **MySQL Exporter**      | Extrait les métriques d’une base de données MySQL               |
| 🐘 **PostgreSQL Exporter** | Extrait les métriques d’une base PostgreSQL                     |

### ⚙️ **Custom Metrics (Métriques personnalisées)** :

> Vous pouvez instrumenter votre application pour **exposer vos propres métriques**, spécifiques à votre domaine métier.

Par exemple :

* Le **nombre de connexions** utilisateurs par minute
* Le **temps de réponse moyen** d’un endpoint
* Le **nombre d’achats** effectués sur un site e-commerce

---

## 📏 **Types de métriques dans Prometheus**

| Type             | Description                                                                                      | Exemple de métrique                                                               |
| ---------------- | ------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------- |
| 🔄 **Counter**   | Compteur **cumulatif** qui **augmente uniquement**. Idéal pour compter des événements.           | `kube_pod_container_status_restarts_total` : nombre de redémarrages de conteneurs |
| 📉 **Gauge**     | Mesure une **valeur instantanée** qui peut monter ou descendre (ex : température, RAM, etc.)     | `container_memory_usage_bytes` : mémoire utilisée                                 |
| 📊 **Histogram** | Mesure des **distributions** (ex : temps de réponse) dans des **plages configurables (buckets)** | `apiserver_request_duration_seconds_bucket`                                       |
| 📐 **Summary**   | Similaire à Histogram mais fournit en plus des **percentiles (quantiles)**                       | `apiserver_request_duration_seconds_sum`                                          |

---

## 🎯 **Objectifs du projet**

| Objectif                                                                     | Description                                                                                                                         |
| ---------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| 🔧 **Implémenter des métriques personnalisées** dans une application Node.js | En utilisant `prom-client`, exposer des métriques telles que le nombre de requêtes, temps de traitement, utilisateurs actifs        |
| 🚨 **Configurer Alertmanager pour envoyer des alertes email**                | Être notifié si un conteneur crash plus de 2 fois (CrashLoop)                                                                       |
| 📑 **Mettre en place la journalisation (logging)**                           | Capturer les logs des applications et des nœuds via la stack **EFK** : Elasticsearch, FluentBit, Kibana                             |
| 🔍 **Implémenter le traçage distribué**                                      | Utiliser **Jaeger** pour tracer les appels entre services et améliorer le débogage dans les architectures complexes (microservices) |

---

## 🏗️ **Architecture du projet**

![Project Architecture](images/architecture.gif)

**Description de l’architecture :**

1. **Application Node.js ou Flask** instrumentée (expose `/metrics`)
2. **Prometheus** récupère automatiquement les métriques exposées
3. **Alertmanager** surveille les métriques critiques (ex : redémarrage de pods) et envoie des alertes par email
4. **Grafana** visualise les données en temps réel à travers des dashboards
5. **EFK (Elasticsearch, FluentBit, Kibana)** collecte et affiche les logs d’applications et du cluster
6. **Jaeger** capture les **traces distribuées** des requêtes entre services


Voici une **version ultra-détaillée et pas-à-pas** de ton cours, spécialement conçue pour qu’un **débutant/junior puisse suivre étape par étape sans se perdre**, et avoir un **résultat fonctionnel** tout en apprenant en profondeur.


## 🧱 **Prérequis avant de commencer**

### ✅ Ce que tu dois avoir fait avant d’attaquer :

1. Avoir un compte AWS et avoir créé une instance EC2 (Ubuntu 22.04 de préférence)
2. Avoir un terminal fonctionnel (SSH ou VSCode Remote SSH connecté à ton EC2)
3. Avoir Docker et Minikube installés sur cette instance
4. Avoir installé `kubectl` et configuré pour Minikube

---

## Étape 1 — ⚙️ **Créer ton application Flask instrumentée**

### 📁 Crée un nouveau dossier de projet :

```bash
mkdir flask-prometheus
cd flask-prometheus
```

### 📝 Crée le fichier `app.py`

```python
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

```

### 🔍 Installe les dépendances :

```bash
pip install flask prometheus_client
```

---

## Étape 2 — 🐳 **Dockerise l’application**

### 📝 Crée un fichier `Dockerfile`

```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install flask prometheus_client
EXPOSE 5000
CMD ["python", "app.py"]
```

### 🛠 Construis l’image Docker :

```bash
docker build -t flask-metrics:v1 .
```

### 🧲 Charge l’image dans Minikube :

```bash
minikube image load flask-metrics:v1
```

---

## Étape 3 — ☸️ **Déploie ton app sur Kubernetes (Minikube)**

### 📝 Crée un fichier `deployment.yaml` :

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: flask-metrics
spec:
  replicas: 1
  selector:
    matchLabels:
      app: flask
  template:
    metadata:
      labels:
        app: flask
    spec:
      containers:
      - name: flask
        image: flask-metrics:v1
        ports:
        - containerPort: 5000
        livenessProbe:
          httpGet:
            path: /metrics
            port: 5000
```

### 📝 Crée un fichier `service.yaml` :

```yaml
apiVersion: v1
kind: Service
metadata:
  name: flask
  labels:
    app: flask   # important : ce label est utilisé par le ServiceMonitor
spec:
  selector:
    app: flask
  ports:
    - name: metrics        # 👈 OBLIGATOIRE pour ServiceMonitor
      port: 80
      targetPort: 5000
  type: ClusterIP

```

### 🚀 Applique-les :

```bash
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```

---

## Étape 4 — 🔍 **Configure Prometheus avec ServiceMonitor**

> On suppose ici que tu as déjà installé `kube-prometheus-stack` (via Helm par ex.)

### 📝 Crée un fichier `flask-monitor.yaml` :

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: flask-monitor
  labels:
    release: prometheus
spec:
  selector:
    matchLabels:
      app: flask
  endpoints:
    - port: "metrics"      # 👈 correspond au nom défini dans le service
      path: /metrics
      interval: 15s

```

### 💡 Applique le fichier :

```bash
kubectl apply -f flask-monitor.yaml
```

---

## Étape 5 — 📬 **Configurer Alertmanager pour envoyer des emails**

### 📝 Crée un fichier `alert.rules.yaml`

```yaml
groups:
- name: pod-restarts
  rules:
  - alert: PodCrashLoop
    expr: increase(kube_pod_container_status_restarts_total[5m]) > 2
    for: 1m
    labels:
      severity: critical
    annotations:
      summary: "Crash détecté sur le pod"
```

### 📝 Crée un fichier `alertmanager.yaml` :

```yaml
global:
  smtp_smarthost: 'smtp.gmail.com:587'
  smtp_from: 'tonmail@gmail.com'
  smtp_auth_username: 'tonmail@gmail.com'
  smtp_auth_password: '{{ .smtp_pass }}'
  smtp_require_tls: true
route:
  receiver: email-notifications
receivers:
  - name: email-notifications
    email_configs:
      - to: 'destinataire@gmail.com'
        send_resolved: true
```

### 📝 Crée le `Secret` Kubernetes :

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: alertmanager-gmail-secret
  namespace: monitoring
type: Opaque
stringData:
  smtp_pass: VOTRE_MDP_APPLICATION
```

> 💌 N’oublie pas d’avoir activé l’option **Mot de passe d’application Gmail**

---

## Étape 6 — 📊 **Ajoute Prometheus dans Grafana**

1. Lance Grafana sur `http://<EC2-IP>:3000`
2. Connecte-toi (`admin/admin` si non modifié)
3. Ajoute Prometheus comme **Data Source**
4. Crée un **dashboard personnalisé** avec ces requêtes :

   * `http_requests_total`
   * `active_users`
   * `request_duration_seconds`
   * `kube_pod_container_status_restarts_total`

---

## Étape 7 — 🧪 **Test de crash et alerte**

### 💣 Force un crash :

```bash
kubectl port-forward svc/flask 8080:80
curl http://localhost:8080/crash
```

### ✅ Vérifie le pod :

```bash
kubectl get pods
```

> 📩 Tu recevras un email d’alerte si le pod redémarre plusieurs fois.

---

## 🔁 Résumé étape par étape (checklist débutant)

| ✅ Étape                      | 📌 Commande/Fichier                      |
| ---------------------------- | ---------------------------------------- |
| Créer app Flask              | `app.py`                                 |
| Installer dépendances        | `pip install flask prometheus_client`    |
| Dockeriser l'app             | `Dockerfile` + `docker build`            |
| Charger image dans Minikube  | `minikube image load`                    |
| Déployer sur Kubernetes      | `deployment.yaml` + `service.yaml`       |
| Instrumenter avec Prometheus | `/metrics` + ServiceMonitor              |
| Ajouter alertes crash        | `alert.rules.yaml` + `alertmanager.yaml` |
| Recevoir alertes par email   | `Secret` + config SMTP                   |
| Visualiser dans Grafana      | Dashboard avec requêtes Prometheus       |



