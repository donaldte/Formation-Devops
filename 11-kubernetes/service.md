
# 🎓 Cours Complet : Les **Services** dans Kubernetes

---

## 🧠 1. Pourquoi les Services existent ?

### 📍 Problème à résoudre

* Les Pods dans Kubernetes sont **éphémères** : si un Pod meurt, il est recréé avec une **nouvelle IP**.
* Impossible de **s’adresser à un Pod directement** de manière fiable dans le temps.
* Kubernetes a besoin d’un moyen de **stabiliser l’accès réseau** à une application.

### ✅ Solution : le **Service**

Un **Service** dans Kubernetes est une **abstraction réseau stable** qui permet :

* De communiquer avec un groupe de Pods de manière **fiable et permanente**.
* De **découvrir automatiquement** les applications (service discovery).
* De **répartir la charge (load balancing)** entre les Pods associés.

---

## 🧩 2. Fonctionnement du Service

* Un Service cible un groupe de **Pods associés par des labels**.
* Il crée une **IP virtuelle stable** (ClusterIP) + un **nom DNS interne**.
* Il utilise un **proxy interne (kube-proxy)** pour diriger le trafic vers les Pods.

### 📌 Exemple :

```text
Utilisateur --> Service --> kube-proxy --> Pod 1, Pod 2, Pod 3 (round-robin)
```

---

## 🔍 3. Types de Services Kubernetes

| Type           | Accessible depuis                      | Load balancing | IP stable ? | Utilisation typique                         |
| -------------- | -------------------------------------- | -------------- | ----------- | ------------------------------------------- |
| `ClusterIP`    | Interne au cluster                     | ✅ Oui          | ✅ Oui       | Communication entre services internes       |
| `NodePort`     | Depuis l’extérieur via un port du nœud | ✅ Oui          | ✅ Oui       | Accès externe simple                        |
| `LoadBalancer` | Internet (via un Cloud Provider)       | ✅ Oui          | ✅ Oui       | Accès public scalable via un LB cloud       |
| `ExternalName` | Redirection DNS                        | ❌              | ❌           | Lien vers un service externe (ex: API SaaS) |

---

## 🟢 1. **ClusterIP** (le **type par défaut**)

### 🎯 But :

Permet à d'autres **applications dans le même cluster** de communiquer avec les Pods **via une IP virtuelle stable**.

### 🌐 Accessibilité :

* ❌ **Pas accessible depuis l’extérieur** (Internet).
* ✅ Accessible **uniquement à l'intérieur du cluster** (ex : depuis un autre Pod).

### 🔁 Load balancing :

✅ Oui. Si plusieurs Pods sont sélectionnés, Kubernetes répartit le trafic entre eux (round-robin).

### 🧪 Exemple :

Tu as un backend (Django) et un frontend (React). Le frontend appelle le backend via l'adresse DNS du service :

```
http://mon-backend-service.default.svc.cluster.local
```

---

## 🟠 2. **NodePort**

### 🎯 But :

Expose ton application **vers l’extérieur du cluster**, en **ouvrant un port sur chaque machine (nœud)**.

### 🌐 Accessibilité :

* ✅ Accessible depuis **ton navigateur**, par l'IP du nœud + le port.
* Port entre **30000–32767** automatiquement attribué (ou défini manuellement).

### 📍 URL d’accès :

```
http://<IP-du-nœud>:<nodePort>
```

> Ex : `http://192.168.99.100:30036`

### 🔁 Load balancing :

✅ Oui. Kube-proxy envoie les requêtes à l’un des Pods disponibles.

### 🧪 Exemple :

Parfait pour tester un service en local avec Minikube :

```bash
kubectl expose deployment monapp --type=NodePort --port=80
```

---

## 🔵 3. **LoadBalancer**

### 🎯 But :

Expose l’application **vers Internet via une IP publique**. Utilisé en **production sur un cloud** (AWS, GCP, Azure...).

### 🌐 Accessibilité :

* ✅ Accessible **depuis l'extérieur du cluster** via une IP **publique** attribuée automatiquement.

### ⚙️ Nécessite :

Un **Cloud Provider** qui gère un Load Balancer (comme AWS ELB).

### 🔁 Load balancing :

✅ Oui. Le Load Balancer cloud répartit les requêtes vers les nœuds → kube-proxy → Pods.

### 🧪 Exemple :

```bash
kubectl expose deployment monapp --type=LoadBalancer --port=80
```

> Sur Minikube, `minikube service monapp` simule un LoadBalancer localement.

---

## 🟣 4. **ExternalName**

### 🎯 But :

Créer un **alias DNS interne** vers un **service externe** (ex : une API SaaS).

### 🌐 Accessibilité :

* ❌ Pas un proxy réel : **pas de load balancing, ni redirection réseau**.
* Juste une redirection **DNS** dans le cluster.

### 📍 Exemple :

Tu veux accéder à une API externe comme :

```text
api.openai.com
```

Tu crées un service Kubernetes :

```yaml
apiVersion: v1
kind: Service
metadata:
  name: api-openai
spec:
  type: ExternalName
  externalName: api.openai.com
```

Dans le cluster, tous les Pods peuvent appeler :

```
http://api-openai.default.svc.cluster.local
```

Et ça redirige vers `api.openai.com`.

---





## 📜 4. Exemple YAML pour chaque type

### 🟢 ClusterIP (par défaut)

```yaml
apiVersion: v1
kind: Service
metadata:
  name: mon-service
spec:
  selector:
    app: monapp
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
```

> 🧠 Redirige les requêtes sur `mon-service:80` vers les Pods qui ont `app: monapp` sur le port 8080.

---

### 🟠 NodePort

```yaml
apiVersion: v1
kind: Service
metadata:
  name: mon-service
spec:
  type: NodePort
  selector:
    app: monapp
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
      nodePort: 30036
```

> Permet d’accéder à l’app via `http://<NodeIP>:30036` depuis l’extérieur du cluster.

---

### 🔵 LoadBalancer

```yaml
apiVersion: v1
kind: Service
metadata:
  name: mon-service
spec:
  type: LoadBalancer
  selector:
    app: monapp
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
```

> Utilise le Load Balancer de ton cloud provider (ex : AWS ELB, GCP LB) pour exposer l’app sur Internet.

---

### 🟣 ExternalName

```yaml
apiVersion: v1
kind: Service
metadata:
  name: mon-service-externe
spec:
  type: ExternalName
  externalName: api.exemple.com
```

> Crée un alias DNS dans le cluster : `mon-service-externe.default.svc.cluster.local` → `api.exemple.com`.

---

## 🌐 5. Découverte de services (Service Discovery)

### 📦 DNS automatique

Chaque Service a un **nom DNS interne** :

```
<nom-service>.<namespace>.svc.cluster.local
```

Exemple :

```bash
curl http://mon-service.default.svc.cluster.local
```

Tu peux aussi utiliser simplement :

```bash
curl http://mon-service
```

si tu es dans le même namespace.

---

## ⚖️ 6. Load Balancing interne

Kubernetes utilise **kube-proxy** :

* Il écoute les ports ouverts par les Services.
* Il redirige le trafic vers un Pod sélectionné **aléatoirement ou en round-robin**.

✅ Il équilibre la charge entre les Pods cibles automatiquement.

---

## 🚀 7. Commandes utiles avec Services

| Commande                                                                        | Description                 |
| ------------------------------------------------------------------------------- | --------------------------- |
| `kubectl get svc`                                                               | Voir tous les Services      |
| `kubectl describe svc mon-service`                                              | Détails du Service          |
| `kubectl expose deployment monapp --port=80 --target-port=8080 --type=NodePort` | Créer un Service rapidement |
| `kubectl delete svc mon-service`                                                | Supprimer un Service        |

---

## ✅ 8. Bonnes pratiques

| Bonne Pratique                                                | Pourquoi ?                                     |
| ------------------------------------------------------------- | ---------------------------------------------- |
| Toujours utiliser des labels cohérents (`app`, `tier`, `env`) | Pour bien associer les Pods au Service         |
| Utiliser `ClusterIP` pour les communications internes         | Plus sécurisé et rapide                        |
| Éviter d’exposer des ports en `NodePort` sans firewall        | Risque de faille de sécurité                   |
| Sur le Cloud, préférer `LoadBalancer` ou `Ingress`            | Pour une gestion avancée                       |
| Activer les **readiness probes** sur les Pods                 | Évite d’envoyer du trafic à des Pods non prêts |

---

## 🧠 Récapitulatif

| Élément      | Description                                            |
| ------------ | ------------------------------------------------------ |
| Service      | Point d’entrée réseau stable vers un ou plusieurs Pods |
| ClusterIP    | Accès interne uniquement                               |
| NodePort     | Accès externe simple (via IP du nœud)                  |
| LoadBalancer | Accès externe via un load balancer (Cloud)             |
| ExternalName | Lien DNS vers une API externe                          |

---

## 🎯 Ce que tu peux faire ensuite :

Souhaites-tu que je t’enseigne :

* 📥 Comment utiliser Ingress pour gérer plusieurs routes HTTP/HTTPS ?
* 🔒 Comment sécuriser les services avec TLS ?
* 📦 Comment associer un Service à un StatefulSet (ex: base de données) ?
* 🧪 Un projet pratique de fin de cours avec plusieurs types de services ?

