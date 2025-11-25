

# 📡 Supervision (Monitoring)

## ✅ Métriques vs Supervision

Les **métriques** sont des mesures ou points de données qui indiquent ce qui se passe.
Par exemple : le nombre de pas que vous faites chaque jour, votre fréquence cardiaque ou la température extérieure sont toutes des métriques.

La **supervision** consiste à surveiller ces métriques dans le temps pour comprendre ce qui est normal, détecter les changements et identifier les problèmes.
C’est comme suivre votre nombre de pas chaque jour pour vérifier si vous atteignez votre objectif de remise en forme, ou surveiller votre fréquence cardiaque pour vous assurer qu’elle reste dans une plage saine.

---

## 🚀 Prometheus

* Prometheus est un outil open-source de surveillance des systèmes et de gestion des alertes, initialement développé par SoundCloud.
* Il est reconnu pour son modèle de données robuste, son puissant langage de requête (**PromQL**) et sa capacité à générer des alertes basées sur des données de séries temporelles.
* Il peut être déployé sur des serveurs physiques ou dans des environnements conteneurisés comme Kubernetes.

---

## 🏠 Architecture de Prometheus

L'architecture de Prometheus est conçue pour être très flexible, évolutive et modulaire.
Elle se compose de plusieurs composants clés, chacun jouant un rôle spécifique dans le processus de surveillance.

![Architecture Prometheus](images/prometheus-architecture.gif)

---

### 🔥 Serveur Prometheus

Le serveur Prometheus est le cœur du système de supervision :

* Il collecte les métriques depuis des cibles configurées.
* Il stocke les données dans sa base de séries temporelles (**TSDB**).
* Il fournit une API HTTP pour les requêtes.

#### Composants :

* **Collecte (Retrieval)** : Scrute les métriques via des points d’accès, soit via une configuration statique, soit via la découverte dynamique.
* **TSDB (Time Series Database)** : Stocke les données collectées, optimisé pour les séries temporelles.
* **Serveur HTTP** : Permet de requêter les données avec PromQL, accéder aux métadonnées et interagir avec d'autres composants.

#### Stockage :

Les données sont stockées localement (disque HDD/SSD) dans un format optimisé pour les séries temporelles.

---

### 🌐 Découverte de Services (Service Discovery)

La découverte de services permet d'identifier automatiquement les cibles à superviser :

* Crucial dans des environnements dynamiques comme Kubernetes.

#### Méthodes :

* **Kubernetes** : Découverte automatique des services, pods et nœuds via l’API Kubernetes.
* **Fichier (File SD)** : Lecture de cibles statiques depuis des fichiers.

---

### 📤 Pushgateway

* Permet d'exposer les métriques de jobs ou applications de courte durée, qui ne peuvent être scrutés directement.
* Ces jobs envoient leurs métriques au **Pushgateway** qui les rend accessibles à Prometheus.

#### Cas d'usage :

* Idéal pour les **jobs batch** ou tâches temporaires.

---

### 🚨 Alertmanager

* Gère les alertes générées par Prometheus.
* Déduplication, regroupement et envoi vers des systèmes de notification comme **PagerDuty, Email ou Slack**.

---

### 🧲 Exporters

* Petites applications qui collectent des métriques d'autres systèmes et les exposent au format Prometheus.

#### Types :

* Node Exporter (métriques matérielles).
* MySQL Exporter (métriques bases de données).
* Autres Exporters spécifiques.

---

### 🖥️ Interface Web de Prometheus

* Interface intégrée pour consulter les métriques, lancer des requêtes PromQL et visualiser les résultats.

---

### 📊 Grafana

* Outil puissant de création de dashboards et de visualisation.
* S’intègre à Prometheus pour des visualisations riches et personnalisées.

---

### 🔌 Clients API

* Les clients API interagissent avec Prometheus via son API HTTP pour récupérer les données et intégrer Prometheus à d'autres systèmes.

---

# 🛠️ Installation & Configuration

## 📦 Étape 1 : Créer un Cluster EKS

### Prérequis :

* Installer AWS CLI → [Documentation AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html).
* Configurer AWS CLI via `aws configure`.
* Installer **eksctl** → [Guide d’installation eksctl](https://eksctl.io/installation/).
* Installer **kubectl** → [Guide d’installation kubectl](https://kubernetes.io/docs/tasks/tools/).

```bash
eksctl create cluster --name=observability \
                      --region=us-east-1 \
                      --zones=us-east-1a,us-east-1b \
                      --without-nodegroup
```

```bash
eksctl utils associate-iam-oidc-provider \
    --region us-east-1 \
    --cluster observability \
    --approve
```

```bash
eksctl create nodegroup --cluster=observability \
                        --region=us-east-1 \
                        --name=observability-ng-private \
                        --node-type=t3.medium \
                        --nodes-min=2 \
                        --nodes-max=3 \
                        --node-volume-size=20 \
                        --managed \
                        --asg-access \
                        --external-dns-access \
                        --full-ecr-access \
                        --appmesh-access \
                        --alb-ingress-access \
                        --node-private-networking

# Mise à jour du fichier kubeconfig
aws eks update-kubeconfig --name observability
```

---

### 🧰 Étape 2 : Installer kube-prometheus-stack

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
```

---

### 🚀 Étape 3 : Déployer le chart dans un namespace "monitoring"

```bash
kubectl create ns monitoring
```

```bash
cd day-2

helm install monitoring prometheus-community/kube-prometheus-stack \
-n monitoring \
-f ./custom_kube_prometheus_stack.yml
```

---

### ✅ Étape 4 : Vérifier l’installation

```bash
kubectl get all -n monitoring
```

#### Interface Prometheus :

```bash
kubectl port-forward service/prometheus-operated -n monitoring 9090:9090
```

**Note :**
Si vous utilisez une instance EC2 ou un serveur cloud, ajoutez l'option :

```bash
--address 0.0.0.0
```

Vous pourrez alors accéder à l'interface via :
`http://<IP-de-votre-instance>:9090`

---

#### Interface Grafana (mot de passe par défaut : `prom-operator`) :

```bash
kubectl port-forward service/monitoring-grafana -n monitoring 8080:80
```

#### Interface Alertmanager :

```bash
kubectl port-forward service/alertmanager-operated -n monitoring 9093:9093
```

---

### 🧼 Étape 5 : Nettoyage

#### Désinstaller le chart Helm :

```bash
helm uninstall monitoring --namespace monitoring
```

#### Supprimer le namespace :

```bash
kubectl delete ns monitoring
```

#### Supprimer le cluster EKS et tout ce qui l’accompagne :

```bash
eksctl delete cluster --name observability
```


