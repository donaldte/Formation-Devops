## 🎯 Objectif

Déployer le jeu 2048 dans un cluster Amazon EKS en utilisant AWS Fargate pour exécuter les pods sans gérer d'infrastructure serveur, et exposer l'application via un Application Load Balancer (ALB) grâce à AWS Load Balancer Controller.

---

## 🛠️ Étapes de déploiement

### 1. **Créer un profil Fargate**

```bash
eksctl create fargateprofile \
  --cluster demo-cluster \
  --region us-west-2 \
  --name alb-sample-app \
  --namespace game-2048
```

Cette commande crée un profil Fargate nommé `alb-sample-app` pour le cluster `demo-cluster` dans la région `us-west-2`. Ce profil spécifie que tous les pods déployés dans le namespace `game-2048` seront exécutés sur AWS Fargate, éliminant ainsi le besoin de gérer des instances EC2.

---

### 2. **Déployer l'application 2048**

```bash
kubectl apply -f https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.5.4/docs/examples/2048/2048_full.yaml
```

Cette commande applique les ressources définies dans le fichier YAML, qui comprend :

* **Namespace** : `game-2048`
* **Deployment** : déploie 5 réplicas du conteneur `docker-2048`
* **Service** : expose l'application sur le port 80
* **Ingress** : configure un ALB pour exposer l'application sur Internet

---

## 📄 Contenu du fichier `2048_full.yaml`

```yaml
---
apiVersion: v1
kind: Namespace
metadata:
  name: game-2048
---
apiVersion: apps/v1
kind: Deployment
metadata:
  namespace: game-2048
  name: deployment-2048
spec:
  selector:
    matchLabels:
      app.kubernetes.io/name: app-2048
  replicas: 5
  template:
    metadata:
      labels:
        app.kubernetes.io/name: app-2048
    spec:
      containers:
      - image: public.ecr.aws/l6m2t8p7/docker-2048:latest
        imagePullPolicy: Always
        name: app-2048
        ports:
        - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  namespace: game-2048
  name: service-2048
spec:
  ports:
    - port: 80
      targetPort: 80
      protocol: TCP
  type: NodePort
  selector:
    app.kubernetes.io/name: app-2048
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  namespace: game-2048
  name: ingress-2048
  annotations:
    alb.ingress.kubernetes.io/scheme: internet-facing
    alb.ingress.kubernetes.io/target-type: ip
spec:
  ingressClassName: alb
  rules:
    - http:
        paths:
        - path: /
          pathType: Prefix
          backend:
            service:
              name: service-2048
              port:
                number: 80
```

---

## 🔍 Explication des composants

* **Namespace `game-2048`** : isole les ressources liées à l'application 2048.
* **Deployment `deployment-2048`** : déploie 5 instances du conteneur `docker-2048`.
* **Service `service-2048`** : expose l'application en interne sur le port 80.
* **Ingress `ingress-2048`** : configure un ALB pour exposer l'application sur Internet. Les annotations spécifient que l'ALB est orienté vers Internet et que les cibles sont des adresses IP (adapté à Fargate).

---

## 🌐 Accéder à l'application

Après quelques minutes, l'ALB sera provisionné. Pour obtenir l'adresse DNS de l'Ingress :

```bash
kubectl get ingress ingress-2048 -n game-2048
```

La colonne `ADDRESS` affichera le nom DNS de l'ALB. Vous pouvez accéder à l'application en ouvrant cette URL dans votre navigateur.


