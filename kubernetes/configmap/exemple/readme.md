

## 🧪 **Objectif**

Créer une app Flask, la dockeriser, la déployer sur Kubernetes avec un ConfigMap pour gérer le port, observer les problèmes, corriger avec un volume, puis utiliser un Secret avec cryptage.

---

## 🧱 Prérequis

* Docker installé
* Minikube ou cluster Kubernetes fonctionnel
* `kubectl` installé et configuré
* Python installé

---

## ✅ Étape 1 – Création du projet Flask

### 📁 Structure

```
kube-flask-configmap/
├── app.py
├── Dockerfile
```

### `app.py`

```python
from flask import Flask
import os

app = Flask(__name__)
PORT = int(os.environ.get("FLASK_PORT", 5000))

@app.route("/")
def hello():
    return f"Hello from Flask running on port {PORT}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
```

---

## 🐳 Étape 2 – Dockerisation

### `Dockerfile`

```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY app.py .

RUN pip install flask

EXPOSE 5000
CMD ["python", "app.py"]
```

### 🔧 Commandes

```bash
docker build -t flask-configmap-app .
minikube image load flask-configmap-app
```

---

## ☸️ Étape 3 – Déploiement sans configmap (hardcoded)

### `deployment.yaml`

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: flask-app
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
        - name: flask-container
          image: flask-configmap-app
          ports:
            - containerPort: 5000
```

### `service.yaml`

```yaml
apiVersion: v1
kind: Service
metadata:
  name: flask-service
spec:
  type: NodePort
  selector:
    app: flask
  ports:
    - protocol: TCP
      port: 80
      targetPort: 5000
```

### 🔧 Commandes

```bash
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
minikube service flask-service
```

---

## 📦 Étape 4 – Ajout d’un ConfigMap pour gérer le port

### `configmap.yaml`

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: flask-config
data:
  FLASK_PORT: "5001"
```

### ⚙️ Mise à jour `deployment.yaml`

Ajoute :

```yaml
        env:
          - name: FLASK_PORT
            valueFrom:
              configMapKeyRef:
                name: flask-config
                key: FLASK_PORT
```

### 🔧 Commandes

```bash
kubectl apply -f configmap.yaml
kubectl delete -f deployment.yaml && kubectl apply -f deployment.yaml
```

---

## ⚠️ Étape 5 – Changement de valeur dans ConfigMap

### Modification `configmap.yaml`

```yaml
data:
  FLASK_PORT: "5002"
```

### 🔧 Commandes

```bash
kubectl apply -f configmap.yaml
kubectl rollout restart deployment flask-app
```

⚠️ **Problème :** sans redémarrage manuel, le pod ne prend pas la nouvelle valeur.

---

## 🔄 Étape 6 – Utilisation de ConfigMap via Volume

### Nouveau `app.py` (lit depuis fichier)

```python
from flask import Flask

app = Flask(__name__)

with open("/config/FLASK_PORT") as f:
    PORT = int(f.read().strip())

@app.route("/")
def hello():
    return f"Hello from Flask (read from file) on port {PORT}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
```

### 🔁 Nouveau `deployment.yaml`

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: flask-app
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
        - name: flask-container
          image: flask-configmap-app
          ports:
            - containerPort: 5000
          volumeMounts:
            - name: config-volume
              mountPath: /config
      volumes:
        - name: config-volume
          configMap:
            name: flask-config
```

### 🔧 Commandes

```bash
docker build -t flask-configmap-app .
minikube image load flask-configmap-app
kubectl apply -f configmap.yaml
kubectl delete -f deployment.yaml && kubectl apply -f deployment.yaml
```

---

## 🔐 Étape 7 – Passage au Secret (base64 auto)

### `secret.yaml`

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: flask-secret
type: Opaque
data:
  FLASK_PORT: NjAwMA==   # "6000" en base64
```

### `app.py` revient à :

```python
from flask import Flask
import os

app = Flask(__name__)
PORT = int(os.environ.get("FLASK_PORT", 5000))

@app.route("/")
def hello():
    return f"Hello from Flask on port {PORT} (from secret)"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
```

### Mise à jour `deployment.yaml`

```yaml
        env:
          - name: FLASK_PORT
            valueFrom:
              secretKeyRef:
                name: flask-secret
                key: FLASK_PORT
```

### 🔧 Commandes

```bash
echo -n "6000" | base64  # pour vérifier
kubectl apply -f secret.yaml
kubectl delete -f deployment.yaml && kubectl apply -f deployment.yaml
```

---

## 🔐 Étape 8 – Cryptage manuel (avancé)

### Ex. : chiffrement avec OpenSSL

```bash
echo -n "6000" | openssl enc -aes-256-cbc -a -salt -pass pass:MyPassword
```

Stocke le résultat chiffré dans un Secret, puis utilise un script Python pour le déchiffrer dans `app.py`. Exercice avancé – peu recommandé sans gestion centralisée des clés (Vault, KMS, etc.).

---

## ✅ Étape 9 – Test final

### 🔧 Commandes pour tout recharger

```bash
kubectl delete -f deployment.yaml
kubectl delete -f service.yaml
kubectl delete -f configmap.yaml
kubectl delete -f secret.yaml

kubectl apply -f configmap.yaml
kubectl apply -f secret.yaml
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml

minikube service flask-service
```

