# 📚 Cours Complet et Professionnel sur les Custom Resource Definitions (CRD) dans Kubernetes avec Minikube et Ecosystème CNCF

## 🌐 Introduction

Dans Kubernetes, tout est un objet : Pods, Services, ConfigMaps... Tous ces objets sont définis par l’API Kubernetes. Cependant, lorsqu’un besoin métier ne peut être représenté par les objets de base, Kubernetes permet d’étendre son API avec les **Custom Resource Definitions (CRD)**. Cela permet aux entreprises de créer leurs propres objets comme s’ils faisaient partie du noyau Kubernetes.

---

## 🎓 Partie 1 : Comprendre la logique globale - CRD, CR, CC (Custom Controller)

### 1.1 🔍 CRD (Custom Resource Definition)

C’est un **type d’objet personnalisé** que vous déclarez à Kubernetes. C’est un peu comme créer un nouveau type de ressource, comme `Pod`, mais propre à votre domaine (ex : `Database`, `Backup`, `Application`, etc).

### 1.2 🧱 CR (Custom Resource)

C’est **une instance de la CRD**. Si la CRD est une classe, le CR est un objet. Vous créez un CR via un manifest YAML pour déclarer une entité.

### 1.3 ⚙️ CC (Custom Controller)

C’est un **programme** qui observe les Custom Resources (CR) et agit en conséquence. Le contrôleur utilise l’API Kubernetes pour surveiller les événements et effectuer des actions (comme créer un Pod, envoyer une requête HTTP, exécuter une commande externe, etc).

### 1.4 🔄 Architecture logique

```
+-------------------------+
|       kubectl          |
+-------------------------+
            |
            v
+-------------------------+       +------------------+
|         CRD            |<----->|  API Server       |
+-------------------------+       +------------------+
            |
            v
+-------------------------+       +-----------------------------+
|       Custom Resource   |-----> |  Custom Controller (Go App) |
+-------------------------+       +-----------------------------+
                                          |
                                          v
                               Actions métiers / Kubernetes API
```

### 1.5 🔄 Exemple réel : ArgoCD

* **CRD** : `Application`
* **CR** : une application GitOps liée à un dépôt Git
* **CC** : synchronise le code Git avec le cluster Kubernetes

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: guestbook
spec:
  source:
    repoURL: https://github.com/argoproj/argocd-example-apps.git
    path: guestbook
    targetRevision: HEAD
  destination:
    server: https://kubernetes.default.svc
    namespace: default
  project: default
```

➡️ Ici, ArgoCD observe cette `Application`, clone le repo et applique les manifests automatiquement dans le cluster.

---

## 📦 Partie 2 : Exemple complet - Déploiement avec CRD + CR + CC

### 2.1 🚀 Objectif : créer une ressource personnalisée `Website` avec son contrôleur

#### Étape 1 - La CRD `website`

```yaml
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: websites.demo.k8s.io
spec:
  group: demo.k8s.io
  versions:
    - name: v1
      served: true
      storage: true
      schema:
        openAPIV3Schema:
          type: object
          properties:
            spec:
              type: object
              properties:
                url:
                  type: string
                owner:
                  type: string
  scope: Namespaced
  names:
    plural: websites
    singular: website
    kind: Website
    shortNames:
      - web
```

#### Étape 2 - Le CR (Custom Resource)

```yaml
apiVersion: demo.k8s.io/v1
kind: Website
metadata:
  name: hooyia-site
spec:
  url: https://www.hooyia.net
  owner: Donald
```

#### Étape 3 - Le contrôleur (Python avec kopf)

```python
import kopf
@kopf.on.create('demo.k8s.io', 'v1', 'websites')
def website_created(spec, **kwargs):
    url = spec.get('url')
    owner = spec.get('owner')
    print(f"🌐 Nouveau site créé : {url} (propriétaire : {owner})")
```

```bash
kopf run controller.py
```

➡️ Résultat : à chaque création de `Website`, le message s'affiche automatiquement dans les logs du contrôleur.

---

## 🏢 Partie 3 : Exemples d’utilisation réelle en entreprise (avec démonstration)

### 🛡️ Istio

* **CRD** : `VirtualService`, `DestinationRule`
* **Usage** : Créer un maillage de service avec règles de routage

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: my-service
spec:
  hosts:
    - myapp.local
  http:
    - route:
        - destination:
            host: myapp
            port:
              number: 80
```

➡️ Cette ressource contrôle le routage des requêtes HTTP au sein du mesh.

### 🔐 Keycloak Operator

* **CRD** : `KeycloakRealm`, `KeycloakUser`
* **Usage** : Déployer des users/realms dans Keycloak à partir de manifest YAML

### 🔁 ArgoCD

* **CRD** : `Application`
* **Usage** : Déployer automatiquement des apps à partir de Git

### 📊 Prometheus Operator

* **CRD** : `ServiceMonitor`
* **Usage** : Ajouter un service à la surveillance Prometheus

---

## 🧠 Partie 4 : Ce qu’il faut retenir

| Terme    | Description                                               |
| -------- | --------------------------------------------------------- |
| CRD      | Custom Resource Definition : définition d’un type d’objet |
| CR       | Custom Resource : instance de cet objet                   |
| CC       | Custom Controller : code qui observe et agit              |
| Operator | Ensemble CRD + CR + Controller appliqué à un domaine      |

