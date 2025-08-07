

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

