# 📘 Cours Complet sur **EFK** et ses Concurrents

## 1. Introduction à la centralisation des logs

Dans les environnements modernes (microservices, containers, Kubernetes), les logs proviennent de multiples sources :

* Conteneurs (Docker, Kubernetes)
* Applications (backend, frontend, batch jobs)
* Infrastructures (serveurs, réseau, cloud)

Sans solution centralisée, il devient difficile de :

* **Rechercher** un événement spécifique
* **Corréler** les logs entre services
* **Analyser** la performance ou les incidents
* **Surveiller** la sécurité (détection d’intrusion)

📌 **But d’un stack EFK** : collecter → centraliser → indexer → visualiser.

---

## 2. Qu’est-ce que EFK ?

**EFK** = **Elasticsearch + Fluentd + Kibana**
C’est une stack open source populaire pour la gestion centralisée des logs.

### 2.1 Elasticsearch (E)

* Moteur de recherche distribué basé sur **Lucene**
* Stocke les logs sous forme de documents JSON indexés
* Recherche ultra-rapide avec API REST
* Supporte le filtrage, l’agrégation et la recherche full-text

📌 **Points clés** :

* Écritures rapides et distribuées
* Indexation par champs → requêtes complexes
* Utilisé aussi pour la recherche de texte, la sécurité (SIEM), etc.

---

### 2.2 Fluentd (F)

* **Agent de collecte et transformation des logs**
* Récupère les logs de différentes sources (fichiers, sockets, conteneurs…)
* Les formate (JSON, CSV, custom) et les envoie à Elasticsearch (ou autre)
* Extensible avec plus de **500 plugins** (S3, Kafka, MongoDB, etc.)

📌 **Rôle clé** : unifier les logs en un format commun (souvent JSON) et les router.

---

### 2.3 Kibana (K)

* Interface graphique pour interroger et visualiser les données d’Elasticsearch
* Crée des dashboards interactifs
* Filtres par date, service, niveau de log (INFO, ERROR…)
* Utilisé pour :

  * Debug d’incidents
  * KPIs en temps réel
  * Sécurité (Elastic SIEM)

---

## 3. Schéma du fonctionnement EFK

```
[Application / Serveur / Conteneur]
           ↓ (logs)
        [Fluentd]
           ↓
   [Elasticsearch Cluster]
           ↓
        [Kibana UI]
```

---

## 4. Avantages de EFK

✅ **Open source** (licence Apache)
✅ Compatible **Kubernetes / Docker**
✅ Évolutif (scalable horizontalement)
✅ Requêtes puissantes (Elasticsearch Query DSL)
✅ Personnalisation avec Fluentd

---

## 5. Limites de EFK

⚠ **Consommation mémoire importante** (surtout Elasticsearch)
⚠ Courbe d’apprentissage pour Elasticsearch DSL
⚠ Maintenance lourde si gros volume de logs (besoin d’un cluster robuste)
⚠ Fluentd peut avoir une latence s’il est mal configuré

---

## 6. Concurrents de EFK

### 6.1 ELK (Elasticsearch – Logstash – Kibana)

* **Logstash** remplace Fluentd comme collecteur/parseur
* Plus ancien que Fluentd, très riche en plugins
* **Différence clé** : Fluentd est plus léger et consomme moins de ressources

---

### 6.2 Loki – Promtail – Grafana

* **Loki** (Grafana Labs) → stockage optimisé pour logs (index minimal)
* **Promtail** → collecte les logs et les envoie à Loki
* **Grafana** → visualisation
* Avantage : faible coût de stockage
* Inconvénient : pas aussi puissant qu’Elasticsearch pour la recherche full-text

---

### 6.3 Graylog

* Basé sur Elasticsearch + MongoDB
* Interface intégrée pour la recherche et l’alerting
* Moins de dépendances que EFK
* Simplicité d’installation mais moins flexible que Kibana

---

### 6.4 Splunk

* **Solution propriétaire** très performante
* Analyse temps réel, machine learning, alertes avancées
* Coût élevé mais fiable pour les entreprises
* Intégrations sécurité (SIEM)

---

### 6.5 OpenSearch – Fluent Bit – OpenSearch Dashboards

* **OpenSearch** = fork open source d’Elasticsearch après changement de licence
* **Fluent Bit** = alternative ultra-légère à Fluentd
* **OpenSearch Dashboards** = fork de Kibana
* Avantage : 100% open source (Apache 2.0)

---

### 6.6 Datadog Logs

* Service SaaS (pas d’installation)
* Collecte, stockage, visualisation, alerting
* Payant à l’usage
* Idéal pour petites équipes sans gestion d’infrastructure

---

## 7. Comparaison synthétique

| Stack                | Collecteur    | Stockage              | Visualisation         | Points forts                                 |
| -------------------- | ------------- | --------------------- | --------------------- | -------------------------------------------- |
| **EFK**              | Fluentd       | Elasticsearch         | Kibana                | Open source, scalable, flexible              |
| **ELK**              | Logstash      | Elasticsearch         | Kibana                | Plugins puissants, historique solide         |
| **Loki**             | Promtail      | Loki DB               | Grafana               | Stockage peu coûteux, simple pour Kubernetes |
| **Graylog**          | Graylog Agent | Elasticsearch+MongoDB | Interface intégrée    | Plus simple que Kibana                       |
| **Splunk**           | Splunk UF     | Splunk Indexer        | Splunk Web            | Très puissant, ML, alertes avancées          |
| **OpenSearch Stack** | Fluent Bit    | OpenSearch            | OpenSearch Dashboards | 100% open source, Amazon support             |
| **Datadog Logs**     | Agent DD      | SaaS                  | SaaS                  | Pas d’infra à gérer, monitoring intégré      |

---

## 8. Bonnes pratiques avec EFK

1. **Limiter la rétention des logs** (30-90 jours)
2. **Indexer par date** pour éviter la surcharge d’Elasticsearch
3. **Utiliser Fluent Bit** pour les environnements à faible ressources
4. **Mettre en place un cluster Elasticsearch multi-nœuds** pour la haute disponibilité
5. **Activer l’alerting** dans Kibana ou via ElastAlert
6. **Compresser les logs archivés** pour réduire le coût stockage

---

## 9. Exemple d’utilisation dans Kubernetes

Environnement Kubernetes avec EFK :

* **Fluentd DaemonSet** → collecte les logs de tous les pods
* **Elasticsearch StatefulSet** → stockage et indexation
* **Kibana Deployment** → interface web

YAML de base pour Fluentd DaemonSet :

```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: fluentd
spec:
  selector:
    matchLabels:
      app: fluentd
  template:
    metadata:
      labels:
        app: fluentd
    spec:
      containers:
      - name: fluentd
        image: fluent/fluentd:v1.14
        env:
        - name: FLUENT_ELASTICSEARCH_HOST
          value: "elasticsearch"
        - name: FLUENT_ELASTICSEARCH_PORT
          value: "9200"
```

---

## 10. Conclusion

* **EFK** est un standard open source pour la gestion des logs
* **Choix de la stack** dépend de :

  * Volume de logs
  * Budget
  * Besoin de recherche full-text
  * Maintenance interne vs SaaS
* Les **concurrents** comme Loki, Graylog, OpenSearch ou Splunk peuvent être plus adaptés selon les cas d’usage.







# 🚀 Guide Complet : EFK + Jaeger sur Minikube avec sécurité Elasticsearch

---

## 🧰 PRÉREQUIS

✔️ Une instance EC2 (Ubuntu recommandé)
✔️ Minikube installé et en cours d’exécution (`minikube start`)
✔️ `kubectl` opérationnel
✔️ `socat` (facultatif)
✔️ Ports suivants ouverts dans les règles de sécurité EC2 :

* 5601 (Kibana)
* 9200 (Elasticsearch via socat ou port-forward)
* 16686 (Jaeger UI)

---

# 📦 ÉTAPE 1 : Créer un Namespace dédié à l’observabilité

```bash
kubectl create namespace observability
```

> 🧠 On isole tous les composants (Elasticsearch, Fluent Bit, Kibana, Jaeger) dans un namespace pour mieux organiser notre cluster.

---

# 🛢️ ÉTAPE 2 : Déployer Elasticsearch avec mot de passe activé

📄 Crée un fichier `elasticsearch.yaml` :

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: elasticsearch
  namespace: observability
spec:
  serviceName: "elasticsearch"
  replicas: 1
  selector:
    matchLabels:
      app: elasticsearch
  template:
    metadata:
      labels:
        app: elasticsearch
    spec:
      containers:
      - name: elasticsearch
        image: docker.elastic.co/elasticsearch/elasticsearch:7.17.0
        ports:
        - containerPort: 9200
        env:
        - name: discovery.type
          value: single-node
        - name: xpack.security.enabled
          value: "true"
        - name: ELASTIC_PASSWORD
          value: "MyStrongPassword123"  # 🔐 Mot de passe de l'utilisateur "elastic"
---
apiVersion: v1
kind: Service
metadata:
  name: elasticsearch
  namespace: observability
spec:
  ports:
  - port: 9200
    name: http
  selector:
    app: elasticsearch
```

🛠️ Applique le manifest :

```bash
kubectl apply -f elasticsearch.yaml
```

---

# 🖥️ ÉTAPE 3 : Déployer Kibana et le connecter à Elasticsearch sécurisé

📄 Crée un fichier `kibana.yaml` :

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: kibana
  namespace: observability
spec:
  replicas: 1
  selector:
    matchLabels:
      app: kibana
  template:
    metadata:
      labels:
        app: kibana
    spec:
      containers:
      - name: kibana
        image: docker.elastic.co/kibana/kibana:7.17.0
        ports:
        - containerPort: 5601
        env:
        - name: ELASTICSEARCH_HOSTS
          value: "http://elastic:MyStrongPassword123@elasticsearch.observability.svc.cluster.local:9200"
---
apiVersion: v1
kind: Service
metadata:
  name: kibana
  namespace: observability
spec:
  ports:
  - port: 5601
    name: http
  selector:
    app: kibana
```

🛠️ Applique :

```bash
kubectl apply -f kibana.yaml
```

---

# 🔍 ÉTAPE 4 : Déployer Fluent Bit avec authentification vers Elasticsearch

📄 Crée le fichier `fluent-bit-configmap.yaml` :

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: fluent-bit-config
  namespace: observability
data:
  fluent-bit.conf: |
    [SERVICE]
        Flush        1
        Daemon       Off
        Log_Level    info
        Parsers_File parsers.conf

    [INPUT]
        Name              tail
        Path              /var/log/containers/*.log
        Parser            docker
        Tag               kube.*
        Refresh_Interval  5
        Skip_Long_Lines  On

    [FILTER]
        Name                kubernetes
        Match               kube.*
        Kube_URL            https://kubernetes.default.svc:443
        Merge_Log           On
        Keep_Log            Off
        K8S-Logging.Parser  On
        K8S-Logging.Exclude On

    [OUTPUT]
        Name  es
        Match *
        Host  elasticsearch.observability.svc.cluster.local
        Port  9200
        HTTP_User  elastic
        HTTP_Passwd  MyStrongPassword123
        Index  fluent-bit
        Type  _doc
        Logstash_Format On
```

📄 Crée maintenant le DaemonSet `fluent-bit-daemonset.yaml` :

```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: fluent-bit
  namespace: observability
spec:
  selector:
    matchLabels:
      name: fluent-bit
  template:
    metadata:
      labels:
        name: fluent-bit
    spec:
      containers:
      - name: fluent-bit
        image: fluent/fluent-bit:1.9
        volumeMounts:
          - name: varlog
            mountPath: /var/log
          - name: config
            mountPath: /fluent-bit/etc/
      volumes:
        - name: varlog
          hostPath:
            path: /var/log
        - name: config
          configMap:
            name: fluent-bit-config
```

🛠️ Applique les deux manifests :

```bash
kubectl apply -f fluent-bit-configmap.yaml
kubectl apply -f fluent-bit-daemonset.yaml
```

---

# 🔭 ÉTAPE 5 : Déployer Jaeger pour les traces distribuées

```bash
kubectl create -f https://github.com/jaegertracing/jaeger-operator/releases/download/v1.46.0/jaeger-operator.yaml -n observability
```

📄 Crée ensuite le fichier `jaeger.yaml` :

```yaml
apiVersion: jaegertracing.io/v1
kind: Jaeger
metadata:
  name: simplest
  namespace: observability
```

```bash
kubectl apply -f jaeger.yaml
```

---

# 🌐 ÉTAPE 6 : Accéder aux Interfaces Web (URL des services)

Voici les commandes pour accéder à chaque service en local ou connaître leur IP/port si tu exposes via NodePort.

---

### 🔗 Voir les services déployés :

```bash
kubectl get svc -n observability
```

🔁 Tu verras une sortie comme :

```
NAME             TYPE        CLUSTER-IP       PORT(S)          AGE
elasticsearch    ClusterIP   10.96.0.1        9200/TCP         5m
kibana           ClusterIP   10.96.0.2        5601/TCP         5m
simplest-query   ClusterIP   10.96.0.3        16686/TCP        3m
```

---

### 🌐 Accès local (avec port-forward)

#### Kibana :

```bash
kubectl port-forward svc/kibana 5601:5601 -n observability
```

> Ouvre [http://localhost:5601](http://localhost:5601)
> Identifiants : `elastic / MyStrongPassword123`

#### Elasticsearch :

```bash
kubectl port-forward svc/elasticsearch 9200:9200 -n observability
```

> Test :

```bash
curl -u elastic:MyStrongPassword123 http://localhost:9200
```

#### Jaeger UI :

```bash
kubectl port-forward svc/simplest-query 16686:16686 -n observability
```

> Ouvre [http://localhost:16686](http://localhost:16686)

---

# ✅ RÉSULTAT ATTENDU

| Composant         | Accès via port-forward                           | Description                                    |
| ----------------- | ------------------------------------------------ | ---------------------------------------------- |
| **Elasticsearch** | [http://localhost:9200](http://localhost:9200)   | Base de données des logs (mot de passe requis) |
| **Kibana**        | [http://localhost:5601](http://localhost:5601)   | Interface Web pour visualiser les logs         |
| **Jaeger UI**     | [http://localhost:16686](http://localhost:16686) | Suivi des requêtes distribuées (spans, traces) |

