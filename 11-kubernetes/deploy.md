
# 🎓 Cours Complet : Le Déploiement dans Kubernetes

## 🧩 1. Introduction à Kubernetes

**Kubernetes** (ou K8s) est une plateforme open source développée par Google pour automatiser le déploiement, la mise à l’échelle et la gestion des applications conteneurisées.

---

## 🔑 2. Concepts Clés

### 📦 2.1 Conteneur (Container)

Un **conteneur** est une unité légère et portable qui contient une application et tout son environnement (bibliothèques, dépendances, etc.). On utilise souvent Docker pour créer les conteneurs.

👉 Exemple :

```bash
docker run nginx
```

---

### 🧱 2.2 Pod

Un **Pod** est l’unité de base de déploiement dans Kubernetes. Il peut contenir **un ou plusieurs conteneurs** qui partagent le même espace réseau (IP, ports) et le même système de fichiers (volumes).

✔️ En général, un Pod contient **un seul conteneur**.
🛠️ Les autres conteneurs sont souvent des **sidecars** (logs, proxy, etc.).

**Exemple de Pod YAML** :

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: mon-pod
spec:
  containers:
    - name: nginx
      image: nginx
```

---

### ♻️ 2.3 ReplicaSet

Un **ReplicaSet** permet d’assurer qu’un nombre donné de **répliques de Pods** sont toujours en cours d’exécution.

💡 Si un Pod tombe, un nouveau est créé automatiquement.

**Exemple** :

```yaml
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: nginx-rs
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx
```

---

### 🚀 2.4 Deployment

Un **Deployment** est l’objet Kubernetes **le plus utilisé pour déployer une application**. Il permet :

* Des **mises à jour progressives** (rolling updates)
* Des **rollbacks**
* De gérer les **ReplicaSets automatiquement**

**Exemple de déploiement** :

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
        - name: nginx
          image: nginx:1.21
```

🧠 Quand vous déployez ce fichier :

1. Kubernetes crée un ReplicaSet
2. Le ReplicaSet crée 3 Pods identiques
3. Si vous mettez à jour l'image, Kubernetes gère la transition (rolling update)

---

## 📊 3. Comparatif : Container, Pod, ReplicaSet, Deployment

| Élément    | Rôle                                          | Géré par |
| ---------- | --------------------------------------------- | -------- |
| Container  | Application avec ses dépendances (Docker)     | Docker   |
| Pod        | Groupe de containers partageant l’IP/port     | K8s      |
| ReplicaSet | Garantit le nombre de Pods souhaité           | K8s      |
| Deployment | Gère les ReplicaSets, mises à jour, rollbacks | K8s      |

---

## 📋 4. Commandes Kubernetes Essentielles

```bash
kubectl create deployment monapp --image=monimage:v1
kubectl get deployments
kubectl get pods
kubectl describe pod monapp-xxxxx
kubectl delete pod monapp-xxxxx
kubectl set image deployment/monapp monapp=monimage:v2
kubectl rollout undo deployment/monapp
kubectl logs monapp-xxxxx
```

---

## ✅ 5. Bonnes Pratiques de Déploiement dans Kubernetes

| Bonne Pratique ✅                            | Explication                             |
| ------------------------------------------- | --------------------------------------- |
| Utilisez des **Deployments**                | Pas de Pods seuls en prod               |
| Ajoutez des **probes** (readiness/liveness) | Pour vérifier la santé des applications |
| Définissez les **ressources** (CPU/mémoire) | Pour éviter de saturer le cluster       |
| Stockez la config via **ConfigMaps**        | Pour séparer config et code             |
| Stockez les secrets via **Secrets**         | Pour les mots de passe, tokens, etc.    |
| Utilisez des **labels intelligents**        | Pour filtrer, scaler et monitorer       |
| Ne jamais utiliser `latest` en prod         | Versionnez vos images                   |
| Mettez en place un **autoscaler**           | Horizontal Pod Autoscaler (HPA)         |
| Organisez vos ressources par **namespace**  | dev, staging, prod                      |

---

## 🏗️ 6. Exemple Complet avec Probes et Resources

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: monapp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: monapp
  template:
    metadata:
      labels:
        app: monapp
    spec:
      containers:
      - name: monapp
        image: monimage:v1.0
        ports:
          - containerPort: 80
        resources:
          requests:
            cpu: "200m"
            memory: "256Mi"
          limits:
            cpu: "500m"
            memory: "512Mi"
        livenessProbe:
          httpGet:
            path: /health
            port: 80
          initialDelaySeconds: 10
          periodSeconds: 5
        readinessProbe:
          httpGet:
            path: /ready
            port: 80
          initialDelaySeconds: 5
          periodSeconds: 5
```

---

## 🔜 7. Suite du Cours : ce que vous pouvez apprendre après

Souhaitez-vous continuer avec :

* 🧪 La mise en place d’un cluster Kubernetes avec Minikube ou K3s ?
* 🌐 L'exposition de vos services (NodePort, LoadBalancer, Ingress) ?
* ⚙️ Le monitoring avec Prometheus, Grafana, Loki ?
* 📈 Le scaling automatique (HPA) ?
* 📦 Un CI/CD GitHub Actions pour déployer automatiquement ?
* 💰 Le déploiement sur AWS (EKS) ?


