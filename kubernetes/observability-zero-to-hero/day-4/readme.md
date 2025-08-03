# 🎛️ **L’Instrumentation : Des Capteurs pour ta Maison Numérique !**

## 📌 **C’est quoi l’instrumentation ?**

**Ce qu’on fait :** L’instrumentation, c’est comme installer des **capteurs dans une maison** pour savoir ce qui s’y passe. Par exemple, un détecteur de fumée te dit s’il y a un feu, ou un compteur d’eau mesure combien tu en utilises. En informatique, on ajoute des **outils** ou du **code** dans une application (comme un site web ou un jeu) pour **surveiller ce qu’elle fait**.

**Rôle :** Ces capteurs collectent trois types d’informations :
- **Métriques** : Des nombres, comme le nombre de personnes qui visitent ton site.
- **Journaux (logs)** : Des messages qui racontent ce qui se passe (ex. : “Quelqu’un a cliqué ici !”).
- **Traces** : Un suivi des actions, comme une carte qui montre le chemin d’une requête dans ton application.

**But :** Savoir si ton application fonctionne bien ou s’il y a un problème à réparer.

**Pourquoi on le fait :** Sans capteurs, c’est comme conduire une voiture sans tableau de bord : tu ne sais pas si tu vas trop vite ou si le moteur chauffe ! L’instrumentation te donne des **yeux magiques** pour voir à l’intérieur de ton programme.

📌 **À retenir :**
- **3 types de données** : Métriques (nombres), logs (messages), traces (suivi).
- **Exemple** : Si ton jeu ralentit, l’instrumentation te dira si c’est à cause d’un bug ou d’un ordinateur surchargé.

---

## 🎯 **Pourquoi on instrumente ?**

**Ce qu’on fait :** On utilise l’instrumentation pour **comprendre et protéger** nos applications, comme si on mettait des alarmes dans une maison.

**Rôle :** L’instrumentation te donne **3 superpouvoirs** :
1. **Voir ce qui se passe 👀** : Comme une caméra qui surveille ton application pour vérifier qu’elle fonctionne.
2. **Mesurer des choses 📏** : Compter des trucs, comme le nombre de clics ou la mémoire utilisée par ton programme.
3. **Réparer vite 🛠** : Trouver pourquoi quelque chose ne marche pas et le corriger rapidement.

**But :** Garder ton application rapide, fiable, et agréable pour tout le monde.

**Pourquoi on le fait :** Imagine que ton site est une fête. Sans capteurs, tu ne sais pas combien d’amis sont venus, s’ils s’amusent, ou si la musique s’est arrêtée. L’instrumentation te donne toutes ces infos pour que la fête soit parfaite !

📌 **À retenir :**
- **3 superpouvoirs** : Voir, Mesurer, Réparer.
- **Exemple** : Si ton site est lent, l’instrumentation te dira si c’est à cause de trop de visiteurs ou d’un bug dans le code.

---

## ⚙️ **Comment on fait pour instrumenter ?**

**Ce qu’on fait :** On installe des **capteurs numériques** dans notre application pour collecter des informations.

**Rôle :** Il y a **2 façons** d’ajouter ces capteurs :
1. **Dans le code** : On ajoute des instructions spéciales dans notre programme pour compter ou mesurer des choses.
2. **Avec des outils** : On utilise des logiciels comme **Prometheus**, qui surveillent automatiquement.

**But :** Rendre la surveillance facile et automatique, pour ne pas avoir à vérifier chaque détail à la main.

**Pourquoi on le fait :** C’est comme installer un thermostat : une fois mis en place, il mesure la température tout seul et t’alerte si besoin.

### Exemple simple (en Python) :
```python
from prometheus_client import Counter

# On crée un capteur qui compte les visites
visites = Counter('visites_total', 'Nombre total de visites')

# À chaque visite, on ajoute 1
visites.inc()
```

**Explication :**
- **Ce qu’on fait** : On crée un “compteur” appelé `visites_total`.
- **Rôle** : Il compte combien de fois quelqu’un visite une page.
- **But** : Savoir si ton site est populaire.
- **Pourquoi** : Plus tu as de visites, plus tu peux améliorer ton site !

📌 **À retenir :**
- **2 façons** : Écrire du code ou utiliser des outils comme **Prometheus**.
- **Prometheus** : Un super outil qui récupère les données via un endroit spécial appelé `/metrics`.

---

## 🧰 **Les outils pour installer des capteurs**

**Ce qu’on fait :** On utilise des **boîtes à outils** (appelées bibliothèques) pour ajouter des capteurs dans nos programmes.

**Rôle :** Chaque langage de programmation (comme Python ou JavaScript) a sa propre boîte à outils pour créer des métriques.

**But :** Faciliter l’ajout de capteurs sans tout programmer de zéro.

**Pourquoi on le fait :** C’est comme utiliser un kit LEGO au lieu de sculpter chaque pièce à la main.

Voici quelques boîtes à outils populaires :

| Langage       | Boîte à outils                  | Rôle                                |
|---------------|--------------------------------|-------------------------------------|
| **Python**    | `prometheus_client`            | Compte les visites, mesure le temps |
| **JavaScript**| `prom-client`                  | Pour les sites web dynamiques       |
| **Java**      | `simpleclient`                 | Pour les grandes applications      |
| **Go**        | `prometheus/client_golang`     | Pour les programmes rapides        |
| **Ruby**      | `prometheus/client_ruby`       | Pour les sites Ruby comme Rails    |

📌 **À retenir :**
- **5 langages** : Python, JavaScript, Java, Go, Ruby.
- Chaque boîte à outils aide à ajouter des **capteurs** facilement.

---

## 🧩 **Instrumentation avec des frameworks**

**Ce qu’on fait :** Certains outils pour créer des sites web (appelés frameworks) ont des **modules spéciaux** qui ajoutent des capteurs automatiquement.

**Rôle :** Ces modules surveillent des choses comme le temps que met une page à charger ou le nombre d’erreurs.

**But :** Gagner du temps en utilisant des outils prêts à l’emploi.

**Pourquoi on le fait :** C’est comme acheter une voiture avec un tableau de bord déjà installé, plutôt que de le construire toi-même.

Exemples de frameworks et leurs modules :

| Framework            | Module                           | Ce qu’il mesure                     |
|----------------------|----------------------------------|-------------------------------------|
| **Flask (Python)**   | `prometheus_flask_exporter`      | Temps de chargement, erreurs        |
| **Express (Node.js)**| `express-prometheus-middleware`  | Nombre de clics, temps de réponse   |
| **Spring Boot (Java)**| `Micrometer`                    | Mémoire, processeur                |
| **FastAPI (Python)** | `prometheus-fastapi-instrumentator`| Temps de réponse, erreurs         |

📌 **À retenir :**
- **4 frameworks** : Flask, Express, Spring Boot, FastAPI.
- Ces modules font le travail **automatiquement** en quelques lignes.

---

## 📈 **Prometheus : Le super-héros des capteurs**

**Ce qu’on fait :** On utilise **Prometheus**, un outil qui **récupère et stocke** toutes les informations de nos capteurs.

**Rôle :** Prometheus va chercher les données dans un endroit spécial de ton application (appelé `/metrics`) et les garde pour qu’on puisse les analyser plus tard.

**But :** Avoir toutes les informations en un seul endroit, comme un carnet de notes magique.

**Pourquoi on le fait :** Sans Prometheus, ce serait comme avoir plein de capteurs dans ta maison, mais sans écran pour voir ce qu’ils disent.

### 🧲 Comment Prometheus fonctionne ?
- **Ce qu’on fait** : On dit à Prometheus d’aller vérifier l’endpoint `/metrics` de notre application.
- **Rôle** : Il utilise des **exporters**, des petits programmes qui traduisent les données en métriques.
- **But** : Collecter des infos sur ton ordinateur, ton site, ou ta base de données.
- **Pourquoi** : Pour surveiller tout, du serveur au jeu vidéo.

Exemples d’exporters :

| Exporter             | Ce qu’il fait                              |
|----------------------|--------------------------------------------|
| **Node Exporter**    | Mesure le CPU, la mémoire, le disque       |
| **MySQL Exporter**   | Surveille une base de données MySQL        |
| **PostgreSQL Exporter**| Surveille une base de données PostgreSQL |

📌 **À retenir :**
- **3 exporters** : Node, MySQL, PostgreSQL.
- **1 endroit clé** : `/metrics` pour donner les données à Prometheus.

---

## 📏 **Les 4 types de capteurs dans Prometheus**

**Ce qu’on fait :** Prometheus utilise **4 types de capteurs** pour surveiller différentes choses dans ton application.

**Rôle :** Chaque capteur a un travail spécifique, comme compter ou mesurer.

**But :** Avoir des informations précises pour mieux comprendre ton application.

**Pourquoi on le fait :** C’est comme avoir différents outils dans une boîte : un marteau pour enfoncer des clous, une règle pour mesurer, etc.

Voici les 4 types :

| Type         | Ce qu’il fait                                      | Exemple                            |
|--------------|--------------------------------------------------|------------------------------------|
| **Counter**  | Compte des choses qui **augmentent**             | Nombre de clics sur un bouton     |
| **Gauge**    | Mesure une valeur qui **change** (monte/descend) | Mémoire utilisée (ex. : 3 Go)     |
| **Histogram**| Regarde la répartition des durées                | Temps pour charger une page       |
| **Summary**  | Comme Histogram, mais avec des stats avancées    | Temps moyen d’une action          |

📌 **À retenir :**
- **4 types** : Counter, Gauge, Histogram, Summary.
- **Exemple** : Un Counter pour compter les clics, une Gauge pour la mémoire.

---

## 🎯 **Les objectifs d’un projet d’instrumentation**

**Ce qu’on fait :** On met en place un projet pour surveiller notre application avec des outils comme Prometheus.

**Rôle :** On veut atteindre **4 objectifs** pour que tout fonctionne bien.

**But :** Faire une application qui marche super bien et qui est facile à réparer.

**Pourquoi on le fait :** C’est comme construire une maison avec des alarmes, des caméras et un tableau de bord pour tout contrôler.

Les 4 objectifs :
1. **Capteurs personnalisés** : Ajouter des compteurs pour des choses précises, comme le nombre de clics.
2. **Alertes email** : Recevoir un message si quelque chose va mal (ex. : l’app plante).
3. **Journaux (logs)** : Garder une trace de tout ce qui se passe avec des outils comme **EFK** (Elasticsearch, FluentBit, Kibana).
4. **Suivi des actions** : Voir le chemin d’une requête dans l’app avec **Jaeger**.

📌 **À retenir :**
- **4 objectifs** : Capteurs, Alertes, Logs, Suivi.
- **Outils** : Prometheus (capteurs), Alertmanager (alertes), EFK (logs), Jaeger (suivi).

---

## 🏗️ **Comment tout s’organise ? (Architecture)**

**Ce qu’on fait :** On construit un système où tous les outils travaillent ensemble, comme une équipe de super-héros.

**Rôle :** Chaque outil a un rôle précis pour surveiller l’application.

**But :** Faire en sorte que tout soit clair et facile à surveiller.

**Pourquoi on le fait :** C’est comme organiser une fête : chaque personne (outil) a un travail (servir à manger, jouer de la musique) pour que tout se passe bien.

Voici l’**architecture type** :

![Architecture d’un projet instrumenté](images/architecture.gif)

**Explication de l’image :**
- **Application** : Ton site ou jeu, qui envoie des données via `/metrics`.
- **Prometheus** : Récupère les données et les stocke.
- **Alertmanager** : Envoie des alertes si quelque chose ne va pas.
- **Grafana** : Affiche des graphiques pour voir les données facilement.
- **EFK** : Collecte les messages (logs) pour savoir ce qui se passe.
- **Jaeger** : Suit les requêtes pour voir où elles vont.

**Rôle de chaque partie :**
1. **Application** : Envoie les données (comme un thermomètre qui donne la température).
2. **Prometheus** : Rassemble toutes les données (comme un carnet de notes).
3. **Alertmanager** : Crie “Alerte !” si quelque chose cloche (comme une alarme).
4. **Grafana** : Montre des graphiques colorés (comme un tableau de bord).
5. **EFK** : Garde un journal des événements (comme un livre d’histoires).
6. **Jaeger** : Trace le chemin des requêtes (comme une carte au trésor).

**But :** Connecter tous ces outils pour avoir une vue complète de ton application.

**Pourquoi :** Sans cette organisation, ce serait le chaos, comme une maison sans plan !

📌 **À retenir :**
- **6 outils** : Application, Prometheus, Alertmanager, Grafana, EFK, Jaeger.
- **1 flux** : L’application envoie des données à Prometheus, qui les partage avec les autres.

---

## 🛠 **Tutoriel : Créer une petite application avec des capteurs**

**Ce qu’on fait :** On va construire une **application simple** avec **Flask** (un outil Python) et ajouter des capteurs avec **Prometheus**. On la mettra sur **Kubernetes** (comme une grande boîte pour ranger des apps) avec **Minikube** (une version mini pour tester).

**Rôle :** Ce tutoriel te montre comment tout connecter, étape par étape.

**But :** Avoir une application surveillée avec des alertes et des graphiques.

**Pourquoi on le fait :** C’est comme construire une petite maison avec des capteurs pour apprendre comment tout fonctionne !

### 📌 **Avant de commencer (Prérequis)**

**Ce qu’on fait :** On vérifie qu’on a tout ce qu’il faut pour commencer.

**Rôle :** S’assurer que notre environnement est prêt, comme vérifier qu’on a tous les ingrédients avant de cuisiner.

**But :** Éviter les problèmes pendant le projet.

**Pourquoi :** Sans ces outils, c’est comme essayer de construire une maison sans marteau !

**4 choses à avoir :**
1. **Compte AWS** : Une machine virtuelle (EC2) avec Ubuntu 22.04.
2. **Terminal SSH** : Pour parler à la machine (comme un téléphone pour appeler ton ordinateur).
3. **Docker et Minikube** : Pour créer et tester l’application.
4. **kubectl** : Un outil pour donner des ordres à Kubernetes.

📌 **À retenir :**
- **4 outils** : AWS, SSH, Docker/Minikube, kubectl.

---

### Étape 1 : Créer une application Flask avec des capteurs

**Ce qu’on fait :** On crée une petite application web avec Flask qui affiche un message et compte des choses, comme les visites.

**Rôle :** L’application est le cœur de notre projet, et les capteurs nous disent ce qu’elle fait.

**But :** Avoir une application qui fonctionne et qui envoie des données à Prometheus.

**Pourquoi :** C’est comme construire une maison et mettre des capteurs pour savoir combien de gens entrent.

1. **Crée un dossier** :
   ```bash
   mkdir ma-super-app
   cd ma-super-app
   ```

2. **Crée le fichier `app.py`** :
   ```python
   from flask import Flask
   from prometheus_client import Counter, Gauge, Histogram, generate_latest
   import time, random, os

   app = Flask(__name__)

   # Capteur pour compter les visites
   VISITES = Counter('visites_total', 'Nombre total de visites')
   # Capteur pour mesurer les utilisateurs
   UTILISATEURS = Gauge('utilisateurs_actifs', 'Nombre d’utilisateurs actifs')
   # Capteur pour mesurer le temps
   TEMPS = Histogram('temps_requete', 'Temps des requêtes')

   @app.route("/")
   def accueil():
       VISITES.inc()  # Compte +1 visite
       UTILISATEURS.set(random.randint(10, 100))  # Simule des utilisateurs
       with TEMPS.time():
           time.sleep(random.uniform(0.1, 0.5))  # Simule un petit délai
       return "Bienvenue dans ma super app !"

   @app.route("/metrics")
   def metrics():
       return generate_latest(), 200, {'Content-Type': 'text/plain'}

   @app.route("/crash")
   def crash():
       os._exit(1)  # Simule un problème

   if __name__ == "__main__":
       app.run(host="0.0.0.0", port=5000)
   ```

3. **Installe les outils nécessaires** :
   ```bash
   pip install flask prometheus_client
   ```

**Explication :**
- **Ce qu’on fait** : On crée une application qui affiche “Bienvenue !” et compte les visites.
- **Rôle** : Les capteurs (`Counter`, `Gauge`, `Histogram`) surveillent les visites, les utilisateurs et le temps.
- **But** : Avoir des données à envoyer à Prometheus.
- **Pourquoi** : Pour tester si nos capteurs marchent bien.

📌 **À retenir :**
- **3 capteurs** : Visites, Utilisateurs, Temps.
- **1 endroit** : `/metrics` pour donner les données à Prometheus.

---

### Étape 2 : Mettre l’application dans une boîte (Docker)

**Ce qu’on fait :** On met notre application dans une “boîte” appelée **Docker** pour qu’elle soit facile à déplacer.

**Rôle :** Docker est comme une boîte magique qui contient tout ce dont l’application a besoin pour fonctionner.

**But :** Faire en sorte que l’application marche partout, pas seulement sur ton ordinateur.

**Pourquoi :** C’est comme mettre un jouet dans une boîte pour l’envoyer à un ami : tout est bien emballé !

1. **Crée un fichier `Dockerfile`** :
   ```dockerfile
   FROM python:3.10-slim
   WORKDIR /app
   COPY . .
   RUN pip install --no-cache-dir flask prometheus_client
   EXPOSE 5000
   CMD ["python", "app.py"]
   ```

2. **Construis la boîte** :
   ```bash
   docker build -t ma-super-app:v1 .
   ```

3. **Envoie la boîte à Minikube** :
   ```bash
   minikube image load ma-super-app:v1
   ```

**Explication :**
- **Ce qu’on fait** : On crée une “boîte” avec tout ce qu’il faut pour l’application.
- **Rôle** : Le `Dockerfile` dit à Docker comment construire la boîte.
- **But** : Préparer l’application pour Kubernetes.
- **Pourquoi** : Pour que l’application soit prête à être utilisée dans un grand système.

📌 **À retenir :**
- **3 étapes** : Créer le `Dockerfile`, construire la boîte, l’envoyer à Minikube.
- **Port 5000** : C’est l’adresse où l’application “habite”.

---

### Étape 3 : Lancer l’application sur Kubernetes

**Ce qu’on fait :** On met notre application dans **Kubernetes**, qui est comme un grand garage pour gérer plein de boîtes Docker.

**Rôle :** Kubernetes s’assure que l’application fonctionne bien et est accessible.

**But :** Faire tourner l’application dans un environnement professionnel.

**Pourquoi :** C’est comme ranger ta boîte dans un garage sécurisé où tout est surveillé.

1. **Crée `deployment.yaml`** :
   ```yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: ma-super-app
   spec:
     replicas: 1
     selector:
       matchLabels:
         app: super-app
     template:
       metadata:
         labels:
           app: super-app
       spec:
         containers:
           - name: super-app
             image: ma-super-app:v1
             imagePullPolicy: Never
             ports:
               - containerPort: 5000
   ```

2. **Crée `service.yaml`** :
   ```yaml
   apiVersion: v1
   kind: Service
   metadata:
     name: super-app
     labels:
       app: super-app
   spec:
     selector:
       app: super-app
     ports:
       - name: metrics
         port: 80
         targetPort: 5000
     type: ClusterIP
   ```

3. **Lance tout** :
   ```bash
   kubectl apply -f deployment.yaml
   kubectl apply -f service.yaml
   ```

**Explanation :**
- **Ce qu’on fait** : On dit à Kubernetes de lancer notre application et de la rendre accessible.
- **Rôle** : Le `deployment.yaml` lance l’application, le `service.yaml` lui donne une adresse.
- **But** : Permettre à Prometheus de trouver l’application.
- **Pourquoi** : Pour que tout soit bien organisé dans notre “garage”.

📌 **À retenir :**
- **2 fichiers** : `deployment.yaml` (lance l’app), `service.yaml` (donne une adresse).
- **1 boîte** : Une seule instance de l’app pour tester.

---

### Étape 4 : Connecter Prometheus

**Ce qu’on fait :** On dit à **Prometheus** de vérifier notre application pour récupérer les données des capteurs.

**Rôle :** Prometheus va chercher les métriques à l’adresse `/metrics` toutes les 15 secondes.

**But :** Collecter les données pour les analyser plus tard.

**Pourquoi :** C’est comme installer un écran qui montre ce que font tes capteurs.

**Prérequis :** Avoir installé `kube-prometheus-stack` (voir la doc officielle si ce n’est pas fait).

1. **Crée `super-app-monitor.yaml`** :
   ```yaml
   apiVersion: monitoring.coreos.com/v1
   kind: ServiceMonitor
   metadata:
     name: super-app-monitor
     labels:
       release: prometheus
   spec:
     selector:
       matchLabels:
         app: super-app
     endpoints:
       - port: metrics
         path: /metrics
         interval: 15s
   ```

2. **Lance le fichier** :
   ```bash
   kubectl apply -f super-app-monitor.yaml
   ```

**Explication :**
- **Ce qu’on fait** : On dit à Prometheus où trouver les métriques.
- **Rôle** : Le `ServiceMonitor` connecte Prometheus à l’application.
- **But** : Récupérer les données automatiquement.
- **Pourquoi** : Pour surveiller sans effort.

📌 **À retenir :**
- **1 fichier** : `ServiceMonitor` pour dire à Prometheus quoi faire.
- **15 secondes** : Prometheus vérifie toutes les 15 secondes.

---

### Étape 5 : Configurer des alertes avec Alertmanager

**Ce qu’on fait :** On configure **Alertmanager** pour qu’il envoie un email si l’application a un problème, comme un crash. On utilise une commande spéciale pour créer un **Secret** sécurisé contenant la configuration d’Alertmanager.

**Rôle :** Alertmanager agit comme une alarme qui envoie un message (par email) quand quelque chose ne va pas. Le Secret protège des informations sensibles, comme la configuration d’envoi d’emails.

**But :** Être averti rapidement si l’application plante, tout en gardant les informations secrètes en sécurité.

**Pourquoi :** C’est comme installer une alarme dans ta maison qui t’envoie un SMS si une fenêtre se casse, mais en gardant le code de l’alarme dans un coffre-fort.

#### 1. **Crée une règle d’alerte (`alert.rules.yaml`)**
**Ce qu’on fait :** On écrit une règle pour dire à Prometheus de surveiller si l’application plante trop souvent.

**Rôle :** Cette règle vérifie si l’application redémarre plus de 2 fois en 5 minutes.

**But :** Déclencher une alerte si quelque chose va mal.

**Pourquoi :** C’est comme mettre un détecteur qui sonne si ta maison a un problème plusieurs fois de suite.

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: alerte-crash
  labels:
    release: monitoring-kube-prometheus
spec:
  groups:
    - name: crash-rules
      rules:
        - alert: CrashApp
          expr: increase(kube_pod_container_status_restarts_total[5m]) > 2
          for: 1m
          labels:
            severity: critical
          annotations:
            summary: "Problème dans l’app !"
            description: "L’app a planté plus de 2 fois en 5 minutes."
```

**Applique la règle :**
```bash
kubectl apply -f alert.rules.yaml
```

**Explication :**
- **Ce qu’on fait** : On crée une règle qui surveille les redémarrages de l’application.
- **Rôle** : La règle dit à Prometheus : “Si l’app plante plus de 2 fois en 5 minutes, alerte !”
- **But** : Détecter les problèmes rapidement.
- **Pourquoi** : Pour ne pas laisser l’application cassée sans le savoir.

---

#### 2. **Crée un mot de passe Gmail**
**Ce qu’on fait :** On génère un mot de passe spécial pour que Alertmanager puisse envoyer des emails via Gmail.

**Rôle :** Ce mot de passe permet à Alertmanager d’utiliser ton compte Gmail en toute sécurité.

**But :** Permettre l’envoi d’emails sans utiliser ton mot de passe principal.

**Pourquoi :** C’est comme donner une clé spéciale à ton alarme pour qu’elle puisse t’appeler sans donner la clé de ta maison.

- Va sur [https://myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords).
- Crée un mot de passe pour “Alertmanager” (ex. : `abcd efgh ijkl mnop`).

**Explication :**
- **Ce qu’on fait** : On obtient un mot de passe sécurisé pour Gmail.
- **Rôle** : Ce mot de passe est utilisé par Alertmanager pour envoyer des emails.
- **But** : Garder ton compte Gmail sécurisé.
- **Pourquoi** : Pour éviter de partager ton vrai mot de passe.

---

#### 3. **Crée un Secret pour la configuration d’Alertmanager**
**Ce qu’on fait :** On crée un fichier `alertmanager.yaml` avec les paramètres d’envoi d’emails, puis on l’ajoute à un **Secret** Kubernetes nommé `alertmanager-main` en utilisant une commande `kubectl`.

**Rôle :** Le Secret stocke le fichier `alertmanager.yaml` de manière sécurisée, car il contient des informations sensibles comme les adresses email et le mot de passe.

**But :** Fournir la configuration d’Alertmanager de façon sécurisée.

**Pourquoi :** C’est comme mettre les instructions de ton alarme dans un coffre-fort que seul Alertmanager peut ouvrir, pour éviter que n’importe qui les lise.

**Crée le fichier `alertmanager.yaml`** :
```yaml
global:
  smtp_smarthost: 'smtp.gmail.com:587'
  smtp_from: 'tonemail@gmail.com'
  smtp_auth_username: 'tonemail@gmail.com'
  smtp_auth_password: 'abcd efgh ijkl mnop'
  smtp_require_tls: true
route:
  receiver: email-notifications
receivers:
  - name: email-notifications
    email_configs:
      - to: 'destinataire@gmail.com'
        send_resolved: true
```

**Crée le Secret avec la commande :**
```bash
kubectl create secret generic alertmanager-main \
  --from-file=alertmanager.yaml=alertmanager.yaml \
  -n monitoring --dry-run=client -o yaml | kubectl apply -f -
```

**Explication de la commande :**
- **Ce qu’on fait** : On crée un Secret nommé `alertmanager-main` qui contient le fichier `alertmanager.yaml`.
- **Rôle** :
  - `--from-file=alertmanager.yaml=alertmanager.yaml` : Ajoute le contenu du fichier `alertmanager.yaml` au Secret.
  - `-n monitoring` : Place le Secret dans le namespace `monitoring`, où Alertmanager est déployé.
  - `--dry-run=client` : Génère le fichier YAML sans l’appliquer immédiatement.
  - `-o yaml | kubectl apply -f -` : Transforme la commande en YAML et l’applique.
- **But** : Stocker la configuration d’Alertmanager de manière sécurisée.
- **Pourquoi** : Les Secrets sont plus sûrs que les ConfigMaps pour les données sensibles comme les mots de passe ou les adresses email.

**Note :** Pour que Alertmanager utilise ce Secret, il faut configurer le déploiement d’Alertmanager pour monter le Secret comme un volume ou une variable d’environnement. Par exemple, tu peux ajouter ceci dans la configuration d’Alertmanager (souvent dans un fichier Helm ou un manifest Kubernetes) :
```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: alertmanager-monitoring-kube-prometheus-alertmanager
  namespace: monitoring
spec:
  template:
    spec:
      containers:
        - name: alertmanager
          volumeMounts:
            - name: alertmanager-config
              mountPath: "/etc/alertmanager"
      volumes:
        - name: alertmanager-config
          secret:
            secretName: alertmanager-main
```

Cette configuration dit à Alertmanager de lire le fichier `alertmanager.yaml` depuis le Secret `alertmanager-main`.

---

#### 4. **Crée un Secret pour le mot de passe Gmail (optionnel)**
**Ce qu’on fait :** Si tu veux séparer le mot de passe Gmail du fichier `alertmanager.yaml` pour plus de sécurité, tu peux créer un autre Secret pour le mot de passe.

**Rôle :** Ce Secret stocke uniquement le mot de passe Gmail, et le fichier `alertmanager.yaml` peut être modifié pour utiliser une variable (comme `{{ .smtp_pass }}`).

**But :** Séparer les données sensibles pour une meilleure sécurité.

**Pourquoi :** C’est comme garder la clé du coffre-fort dans un endroit différent des instructions.

**Commande pour créer le Secret du mot de passe (optionnel) :**
```bash
kubectl create secret generic alertmanager-gmail-secret \
  --from-literal=smtp_pass='abcd efgh ijkl mnop' \
  -n monitoring --dry-run=client -o yaml | kubectl apply -f -
```

**Modifier `alertmanager.yaml` (si tu utilises cette option) :**
```yaml
global:
  smtp_smarthost: 'smtp.gmail.com:587'
  smtp_from: 'tonemail@gmail.com'
  smtp_auth_username: 'tonemail@gmail.com'
  smtp_auth_password: '{{ .smtp_pass }}'
  smtp_require_tls: true
route:
  receiver: email-notifications
receivers:
  - name: email-notifications
    email_configs:
      - to: 'destinataire@gmail.com'
        send_resolved: true
```

**Explication :**
- **Ce qu’on fait** : On crée un Secret séparé pour le mot de passe Gmail.
- **Rôle** : Le Secret `alertmanager-gmail-secret` stocke le mot de passe, et `alertmanager.yaml` utilise une variable pour le récupérer.
- **But** : Améliorer la sécurité en séparant les données sensibles.
- **Pourquoi** : Cela rend la configuration plus flexible et sécurisée.

**Note :** Cette étape est facultative. Si le mot de passe est déjà dans `alertmanager.yaml` (comme dans le Secret `alertmanager-main`), tu n’as pas besoin de ce Secret supplémentaire. J’inclus cette option pour montrer une pratique courante dans les environnements professionnels.

---

#### 5. **Redémarre Alertmanager**
**Ce qu’on fait :** On redémarre Alertmanager pour qu’il utilise la nouvelle configuration du Secret.

**Rôle :** Le redémarrage applique les changements du Secret `alertmanager-main` (et optionnellement `alertmanager-gmail-secret`).

**But :** S’assurer que Alertmanager est prêt à envoyer des emails.

**Pourquoi :** C’est comme redémarrer ton téléphone après avoir installé une nouvelle application.

```bash
kubectl rollout restart statefulset alertmanager-monitoring-kube-prometheus-alertmanager -n monitoring
```

**Explication :**
- **Ce qu’on fait** : On relance Alertmanager.
- **Rôle** : La commande dit à Kubernetes de mettre à jour Alertmanager avec la nouvelle configuration.
- **But** : Activer les nouvelles règles et configurations.
- **Pourquoi** : Pour que tout fonctionne correctement.

---

📌 **À retenir pour l’Étape 5 :**
- **2 ou 3 fichiers/commandes** : Règle d’alerte (`alert.rules.yaml`), Secret pour la configuration (`alertmanager-main`), et optionnellement Secret pour le mot de passe (`alertmanager-gmail-secret`).
- **1 règle** : Alerte si l’app plante **2 fois** en **5 minutes**.
- **1 email** : Envoyé via Gmail quand l’alerte se déclenche.
- **Pourquoi utiliser un Secret au lieu d’un ConfigMap ?** Les Secrets sont plus sûrs pour les données sensibles, comme les mots de passe ou les adresses email, car ils sont chiffrés dans Kubernetes.

---

### Étape 6 : Tester l’alerte

**Ce qu’on fait :** On fait planter l’application pour voir si l’alerte fonctionne.

**Rôle :** Tester si notre système d’alarme envoie bien un email.

**But :** S’assurer que tout est bien configuré.

**Pourquoi :** C’est comme tester une alarme de maison pour vérifier qu’elle sonne.

1. **Accède à l’application** :
   ```bash
   kubectl port-forward svc/super-app 8080:80
   ```

2. **Provoque un crash** :
   ```bash
   curl http://localhost:8080/crash
   ```

3. **Vérifie les redémarrages** :
   ```bash
   kubectl get pods
   ```

**Explication :**
- **Ce qu’on fait** : On fait exprès de casser l’app pour voir si l’alerte fonctionne.
- **Rôle** : La commande `curl` simule un problème, et `kubectl` montre si l’app redémarre.
- **But** : Confirmer que l’email arrive.
- **Pourquoi** : Pour être sûr que notre alarme fonctionne.

📌 **À retenir :**
- **1 test** : Si l’app plante **2 fois** en **5 minutes**, tu reçois un email.

---

### Étape 7 : Voir les résultats avec Grafana

**Ce qu’on fait :** On utilise **Grafana** pour voir nos données sous forme de jolis graphiques.

**Rôle :** Grafana transforme les nombres en images faciles à comprendre.

**But :** Visualiser ce qui se passe dans l’application.

**Pourquoi :** C’est comme avoir un tableau de bord dans une voiture pour voir ta vitesse et ton essence.

1. Ouvre Grafana : `http://<IP_EC2>:3000` (identifiants : `admin/admin`).
2. Ajoute Prometheus comme source : `http://prometheus-kube-prometheus-prometheus.monitoring:9090`.
3. Crée un tableau de bord avec :
   - `visites_total` (nombre de clics).
   - `temps_requete` (temps de chargement).
   - `kube_pod_container_status_restarts_total` (redémarrages).

**Explication :**
- **Ce qu’on fait** : On configure Grafana pour montrer nos métriques.
- **Rôle** : Grafana affiche des graphiques pour voir les données facilement.
- **But** : Comprendre ce qui se passe sans lire des chiffres compliqués.
- **Pourquoi** : Pour rendre la surveillance amusante et claire.

📌 **À retenir :**
- **3 métriques** : Clics, temps, redémarrages.
- **1 tableau** : Pour tout voir en un coup d’œil.

---

## ✅ **Checklist pour tout vérifier**

**Ce qu’on fait :** On passe en revue tout ce qu’on a fait pour s’assurer que rien n’a été oublié.

**Rôle :** Vérifier que chaque étape est complète.

**But :** Avoir une application qui fonctionne et qui est surveillée.

**Pourquoi :** C’est comme vérifier qu’une maison est bien construite avant d’emménager.

| Étape                     | Détails                              |
|---------------------------|--------------------------------------|
| Créer l’app Flask         | `app.py` avec `/metrics`             |
| Mettre dans Docker        | `Dockerfile` + `docker build`        |
| Lancer sur Kubernetes      | `deployment.yaml` + `service.yaml`   |
| Connecter Prometheus      | `ServiceMonitor` toutes les 15s      |
| Configurer Alertmanager   | Alertes email pour 2 crashes/5min    |
| Tester                    | `curl /crash` + vérifier email       |
| Visualiser avec Grafana   | Graphiques pour 3 métriques          |

📌 **À retenir :**
- **7 étapes** pour tout faire.
- **1 résultat** : Une app surveillée avec alertes et graphiques.

