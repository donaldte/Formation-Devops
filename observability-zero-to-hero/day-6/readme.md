# 🕵️‍♂️ Qu’est-ce que Jaeger ?

Jaeger est un système open source de traçage distribué de bout en bout, utilisé pour la supervision et le débogage d’architectures basées sur les microservices.
Il aide les développeurs à comprendre comment les requêtes circulent dans un système complexe, en retraçant le chemin suivi et en mesurant la durée de chaque étape.

---

## ❓ Pourquoi utiliser Jaeger ?

Dans les applications modernes (surtout en microservices), une seule requête utilisateur peut passer par plusieurs services. Quand un problème survient, il est difficile d’identifier la source. Jaeger aide à :

* 🐢 **Identifier les goulots d’étranglement** : voir où l’application consomme le plus de temps.
* 🔍 **Trouver la cause des erreurs** : remonter à la source des problèmes.
* ⚡ **Optimiser les performances** : comprendre et réduire la latence des services.

---

## 📚 Concepts de base

* 🛤️ **Trace** : représente le parcours complet d’une requête entre plusieurs services.
* 📏 **Span** : une opération unique dans une trace (exemple : appel API, requête SQL). Elle a un temps de début et une durée.
* 🏷️ **Tags** : paires clé-valeur ajoutant du contexte (ex. méthode HTTP, code retour).
* 📝 **Logs** : informations détaillées sur ce qui s’est passé durant un span.
* 🔗 **Propagation de contexte** : permet de transmettre les infos de trace entre services afin de garder la continuité.

---

# 🏠 Architecture Jaeger

Jaeger se compose de plusieurs éléments :

* **Agent** : collecte les traces des applications.
* **Collector** : reçoit et traite les traces.
* **Query** : fournit l’UI pour visualiser les traces.
* **Stockage** : conserve les traces (par défaut en mémoire dans Minikube).

![Project Architecture](images/architecture.gif)
---

## ⚙️ Mise en place de Jaeger dans Minikube

### Étape 1 : Instrumentation du code

On doit instrumenter nos services avec OpenTelemetry pour générer et envoyer des traces.
👉 Dans ton cas, ton application Flask est déjà instrumentée avec OpenTelemetry (cf. code `app.py`).

---

### Étape 2 : Créer le namespace d’observabilité

```bash
kubectl create ns observability
```

---

### Étape 3 : Ajouter le dépôt Helm de Jaeger

```bash
helm repo add jaegertracing https://jaegertracing.github.io/helm-charts
helm repo update
```

---

### Étape 4 : Installer Jaeger (all-in-one)

👉 Ce mode déploie tous les composants Jaeger (collector, query, agent, stockage mémoire) dans un seul pod.

```bash
helm install jaeger jaegertracing/jaeger -n observability \
  --set allInOne.enabled=true \
  --set collector.service.type=ClusterIP \
  --set query.service.type=NodePort
```

---

### Étape 5 : Port-forward pour accéder à l’UI Jaeger

```bash
kubectl -n observability port-forward svc/jaeger-query 16686:16686
```

Puis ouvre dans ton navigateur :
👉 [http://localhost:16686](http://localhost:16686)

---

## 🧼 Nettoyage

Si tu veux désinstaller :

```bash
helm uninstall jaeger -n observability
kubectl delete ns observability
```