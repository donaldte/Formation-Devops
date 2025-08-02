# 🎓 **Cours Complet : Prometheus & Grafana pour Monitorer une App Flask dans Minikube (sur EC2)**

---

## 📌 **Plan Global**

1. Architecture globale
2. Pourquoi monitorer Flask dans Kubernetes ?
3. Installation de Minikube sur EC2
4. Déployer l'application Flask (Deployment + Service)
5. Installer Prometheus & Grafana (avec Helm)
6. Configurer le Service en NodePort (et pourquoi)
7. Visualiser avec le Dashboard Grafana ID 3662
8. Liste complète des métriques essentielles
9. Conclusion et Bonnes pratiques

---

---

## ✅ 1. Architecture Globale

```
                 +---------------------+
                 |  EC2 Instance (AWS) |
                 |---------------------|
                 |  Minikube Cluster   |
                 |                     |
                 | +-----------------+ |
                 | | Flask App       | |
                 | |  (K8s Deploy)   | |
                 | +-----------------+ |
                 | +-----------------+ |
                 | | Prometheus      | |
                 | +-----------------+ |
                 | +-----------------+ |
                 | | Grafana         | |
                 | +-----------------+ |
                 +---------------------+
```

---

## ✅ 2. Pourquoi Monitorer Flask dans Kubernetes ?

* **Suivre la charge CPU, RAM de l'app Flask**.
* Visualiser les **requêtes HTTP** et leur durée.
* Voir le **nombre de pods actifs** et leur état.
* Avoir des **alertes** en cas de surcharge ou de panne.
* Surveiller tout le cluster Kubernetes.

---

## ✅ 3. Installer Minikube sur EC2

> Utilise une EC2 avec au moins **4GB RAM** & **2vCPU** (Instance recommandée : `t3.medium`)

### Installation :

```bash
sudo yum update -y
sudo yum install -y conntrack
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl && sudo mv kubectl /usr/local/bin/

# Lance Minikube en mode Docker (ou autre driver si besoin)
minikube start --driver=docker
```

---

## ✅ 4. Déployer ton Application Flask dans Kubernetes

### Exemple `app.py` (ton app Flask exposant des métriques) :

```python
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
```

### Dockerfile :

```Dockerfile
FROM python:3.10
RUN pip install flask prometheus_client
COPY app.py .
CMD ["python", "app.py"]
```

### Kubernetes Deployment & Service :

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: flask-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: flask-app
  template:
    metadata:
      labels:
        app: flask-app
    spec:
      containers:
      - name: flask-app
        image: <ton-image-docker>
        ports:
        - containerPort: 5000
---
apiVersion: v1
kind: Service
metadata:
  name: flask-service
spec:
  type: NodePort  # ⚠️ Important pour accès externe
  selector:
    app: flask-app
  ports:
  - port: 5000
    targetPort: 5000
```

> 🎯 **Pourquoi `NodePort` ?**

* Permet d'exposer le service sur un port accessible depuis l'extérieur (indispensable sur EC2).
* Sans LoadBalancer dans Minikube, NodePort est la seule option simple.

---

## ✅ 5. Installer Prometheus & Grafana avec Helm

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm install monitoring prometheus-community/kube-prometheus-stack
```

### Vérifie :

```bash
kubectl get pods
kubectl get svc
```

---

## ✅ 6. Exposer Prometheus et Grafana avec NodePort

> Modification via Helm :

```bash
helm upgrade --install monitoring prometheus-community/kube-prometheus-stack \
  --set grafana.service.type=NodePort \
  --set prometheus.service.type=NodePort
```

### obtenir le mot de passe de l'utilisateur admin
```bash
kubectl --namespace default get secrets monitoring-grafana -o jsonpath="{.data.admin-password}" | base64 -d ; echo
```

### Obtenir les URLs :

```bash
# Accès à Prometheus
minikube service monitoring-kube-prometheus-prometheus --url

# Accès à Grafana
minikube service monitoring-grafana --url

```

---

## ✅ 7. Visualiser avec Grafana Dashboard 3662 (Kubernetes Cluster Monitoring)

* Va sur Grafana.
* Import Dashboard :

  1. Menu → **Import**
  2. ID : `3662`
  3. Choisis la datasource : `Prometheus`

🎯 **Pourquoi ce Dashboard ?**

* Vue complète de tout le cluster Kubernetes :

  * CPU, RAM, Pods, Nodes, Network, Disk I/O.
* Clé pour diagnostiquer des pannes.
* Inclus des détails avancés sur :

  * Pods en erreur
  * Saturation mémoire
  * Performance des containers.

---

## ✅ 8. Liste Complète des Métriques Essentielles à Collecter

### 📈 **Métriques Kubernetes via Prometheus**

| Catégorie | Métriques                                                                          | Description               |
| --------- | ---------------------------------------------------------------------------------- | ------------------------- |
| CPU       | `container_cpu_usage_seconds_total`                                                | Utilisation CPU           |
| RAM       | `container_memory_usage_bytes`                                                     | Consommation mémoire      |
| Disque    | `container_fs_usage_bytes`                                                         | Utilisation du disque     |
| Réseau    | `container_network_receive_bytes_total` / `container_network_transmit_bytes_total` | Trafic réseau             |
| Pod       | `kube_pod_status_phase`                                                            | État du pod               |
| Node      | `node_cpu_seconds_total`, `node_memory_MemAvailable_bytes`                         | Utilisation du node       |
| Requests  | `flask_request_count` (ta métrique custom)                                         | Nombre de requêtes Flask  |
| Latence   | Avec histogrammes Prometheus si ajoutés dans Flask                                 | Temps de réponse          |
| Status    | `up`                                                                               | Cibles accessibles ou non |

---

### 📊 **Métriques Importantes pour Flask (Custom App)**

| Métrique                     | Description                                                 |
| ---------------------------- | ----------------------------------------------------------- |
| `flask_request_count`        | Nombre total de requêtes                                    |
| Temps de réponse (optionnel) | Durée des requêtes (ajouter Histogram dans Flask si besoin) |

---

## ✅ 9. Conclusion et Bonnes Pratiques

* **Prometheus** : Collecte & stockage des métriques.
* **Grafana** : Visualisation & Alertes.
* **Dashboard 3662** : Idéal pour avoir une vue complète du cluster.
* Toujours :

  * Exposer les services internes via **NodePort** sur EC2.
  * Personnaliser les dashboards pour tes propres métriques.

---

## ✅ 🎁 Bonus : Commandes Utiles

```bash
# Supprimer toute la stack
helm uninstall monitoring

# Re-synchroniser Prometheus
kubectl rollout restart deployment monitoring-kube-prometheus-stack-prometheus

# Vérifier les metrics Flask
curl http://<ip-node>:<nodeport>/metrics
```



### 📋 Redirection des Ports avec Socat**

Dans ce script, nous utilisons la commande **socat** pour rediriger des ports internes de Minikube vers l'extérieur (accessible depuis Internet via l'IP publique de l'EC2) :

```bash
sudo socat TCP-LISTEN:31869,fork TCP:192.168.58.2:31869 &
sudo socat TCP-LISTEN:30924,fork TCP:192.168.58.2:30924 &
sudo socat TCP-LISTEN:30090,fork TCP:192.168.58.2:30090 &
```

#### 🎯 Pourquoi fait-on cela ?

Minikube, lorsqu'il utilise le driver **Docker**, expose ses services sur un réseau interne Docker (généralement sur l'IP privée `192.168.58.2`).
Même si les ports NodePort sont ouverts dans Kubernetes et dans le pare-feu AWS, ils **ne sont pas accessibles directement depuis l’extérieur** car Minikube ne les publie pas sur l'interface réseau principale de l'EC2.

#### 🛠️ Solution : Port Forwarding avec Socat

* **socat** écoute sur le port externe de l'EC2 (ex. 30853 pour Grafana).
* Dès qu’une connexion arrive, il la redirige vers l'IP interne de Minikube (`192.168.58.2`) et le port correspondant.
* Cela agit comme un "pont" ou proxy TCP entre l'extérieur et Minikube.

#### 🔗 Dans ce cas :

| Port EC2 | Service    | Port Minikube | Utilisation     |
| -------- | ---------- | ------------- | --------------- |
| 30853    | Grafana    | 30853         | Monitoring      |
| 30090    | Prometheus | 30090         | Metrics         |
| 31129    | Flask App  | 31129         | Application Web |

#### ✅ Avantage :

* Simple, efficace, immédiat.
* Permet d’accéder aux dashboards et à l’app Flask depuis l’extérieur sans modifier la configuration Minikube.

#### ⚠️ Attention :

* Cette redirection est temporaire (si la machine redémarre, il faut relancer les commandes).
* Pour une solution permanente, il est recommandé d’utiliser un service `systemd` ou une autre solution d'automatisation.

