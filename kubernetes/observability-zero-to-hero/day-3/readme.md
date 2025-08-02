

# 🧠 **Cours Complet PromQL (Prometheus Query Language)**

---

## 🔍 **1. Introduction à Prometheus & PromQL**

**Prometheus** est un système de surveillance (monitoring system) open source conçu pour collecter des **métriques** (metrics) sous forme de **séries temporelles** (time series data).
**PromQL** est le **langage de requête** (query language) de Prometheus qui permet d’interroger, d’agréger et de manipuler ces données.

---

## 📊 **2. Comprendre les Métriques (Metrics)**

### 🔹 Type de métriques :

1. `counter` (compteur) : valeur qui **augmente uniquement**, ex. nombre de requêtes.
2. `gauge` (jauge) : valeur qui **peut monter et descendre**, ex. mémoire utilisée.
3. `histogram` (histogramme) : distribution des valeurs en **buckets** (tranches).
4. `summary` : similaire à histogram, mais calcule aussi les **quantiles**.

---

## 🏷️ **3. Les Étiquettes (Labels)**

Les **labels** sont des paires `clé="valeur"` (key-value pairs) qui ajoutent des **dimensions** aux métriques.

### Exemple :

```bash
http_requests_total{method="GET", handler="/api", status="200"}
```

* `http_requests_total` → nom de la métrique.
* `{method="GET", handler="/api", status="200"}` → **labels** qui ajoutent des détails.

---

## ⏱️ **4. Séries Temporelles (Time Series)**

Chaque combinaison de **nom de métrique + labels** forme une **série temporelle unique**.

Exemple :

```bash
container_cpu_usage_seconds_total{pod="api-server-1"}
```

---

## 🔍 **5. Syntaxe de base PromQL**

| Élément              | Description                                                |
| -------------------- | ---------------------------------------------------------- |
| `metric_name`        | Nom de la métrique (metric)                                |
| `{label="value"}`    | Filtrage exact sur les étiquettes                          |
| `{label=~"regex.*"}` | Filtrage avec expressions régulières (regular expressions) |
| `[5m]`               | Sélecteur de plage de temps (range vector)                 |
| `@timestamp`         | Ancrage temporel spécifique (timestamp selector)           |

---

## 💡 **6. Requêtes de base (Instant Queries)**

| Requête                                             | Description                                            |
| --------------------------------------------------- | ------------------------------------------------------ |
| `up`                                                | Retourne l’état de tous les targets (1 = UP, 0 = DOWN) |
| `container_memory_usage_bytes{namespace="default"}` | Utilisation mémoire dans le namespace `default`        |
| `rate(http_requests_total[1m])`                     | Taux de requêtes HTTP par seconde                      |

---

## 🕒 **7. Requêtes sur plage de temps (Range Queries)**

Ces requêtes analysent une **plage de données** sur un intervalle :

```bash
rate(container_cpu_usage_seconds_total{job="kubelet"}[5m])
```

---

## 🧮 **8. Agrégation (Aggregation Operators)**

Les opérateurs d’agrégation permettent de **regrouper** ou **résumer** les séries :

| Opérateur         | Description                    |
| ----------------- | ------------------------------ |
| `sum()`           | Somme                          |
| `avg()`           | Moyenne                        |
| `min()`           | Minimum                        |
| `max()`           | Maximum                        |
| `count()`         | Nombre de séries               |
| `stddev()`        | Écart-type                     |
| `stdvar()`        | Variance                       |
| `topk(k, ...)`    | Top K valeurs les plus élevées |
| `bottomk(k, ...)` | Top K valeurs les plus faibles |

### 🔧 Exemple d’utilisation :

```bash
sum(rate(container_cpu_usage_seconds_total[5m])) by (namespace)
```

---

## ➕ **9. Opérations arithmétiques**

Vous pouvez faire des opérations mathématiques sur les métriques :

```bash
(rate(http_requests_total[1m]) / rate(cpu_usage_seconds_total[1m])) * 100
```

---

## 📦 **10. Fonctions utiles dans PromQL**

| Fonction               | Utilité                                                     |
| ---------------------- | ----------------------------------------------------------- |
| `rate()`               | Taux de variation par seconde sur des métriques `counter`   |
| `irate()`              | Taux instantané                                             |
| `increase()`           | Variation totale sur un intervalle                          |
| `delta()`              | Différence brute entre premier et dernier point             |
| `deriv()`              | Dérivée instantanée                                         |
| `predict_linear()`     | Prédiction linéaire                                         |
| `histogram_quantile()` | Calcul d’un percentile sur une métrique de type `histogram` |
| `abs()`, `ceil()`, etc | Fonctions mathématiques classiques                          |

---

## 📈 **11. Quantiles avec `histogram_quantile()`**

Permet d’extraire des quantiles (comme le 95e percentile) depuis une distribution histogramme.

```bash
histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))
```

---

## 🧰 **12. Opérateurs de comparaison & logique**

| Opérateur | Signification |
| --------- | ------------- |
| `==`      | Égal          |
| `!=`      | Différent     |
| `>`       | Supérieur     |
| `<`       | Inférieur     |
| `and`     | ET logique    |
| `or`      | OU logique    |
| `unless`  | Sauf          |

### Exemple :

```bash
up == 0
```

→ Affiche les targets qui sont **DOWN**.

---

## 🔄 **13. Joins & Matching entre séries**

PromQL permet de **joindre** deux ensembles de séries :

```bash
http_requests_total / container_restarts_total
```

Vous pouvez spécifier les **labels de jointure** :

```bash
rate(a[5m]) / ignoring(instance) rate(b[5m])
```

---

## 🧪 **14. Bonnes pratiques PromQL**

* Utiliser `rate()` au lieu de `increase()` pour les tableaux de bord en temps réel.
* Ajouter `by(...)` pour grouper proprement les données.
* Ne pas utiliser trop d'expressions régulières : elles sont **coûteuses**.
* Toujours tester avec des **requêtes simples** d’abord.

---

## 🧠 **15. Cas pratiques**

### 🔍 CPU élevé sur un pod :

```bash
topk(5, rate(container_cpu_usage_seconds_total{namespace="prod"}[1m]))
```

### 📉 Requêtes lentes à l’API :

```bash
histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, handler))
```

### 🔁 Nombre de redémarrages de conteneurs :

```bash
increase(kube_pod_container_status_restarts_total[1h])
```

---

## 🧱 **16. Expressions combinées avec alertes**

PromQL est aussi utilisé pour **les alertes** via les règles :

```yaml
- alert: HighPodRestarts
  expr: increase(kube_pod_container_status_restarts_total[5m]) > 5
  for: 5m
  labels:
    severity: warning
  annotations:
    description: "Plus de 5 redémarrages détectés dans les 5 dernières minutes."
```

---

## 🧩 **17. Outils autour de PromQL**

* **Grafana** : pour visualiser les requêtes PromQL.
* **Alertmanager** : pour les alertes basées sur PromQL.
* **Thanos / Cortex** : pour l’**extension** de Prometheus à grande échelle.
* **PromLens** : outil visuel pour composer et analyser des requêtes PromQL.

---

## ✅ **Conclusion**

Avec PromQL, vous pouvez analyser des métriques complexes, observer l’état d’un système, diagnostiquer des incidents, créer des tableaux de bord et générer des alertes efficaces. C’est un outil **incontournable** dans la stack **DevOps / SRE** moderne.

