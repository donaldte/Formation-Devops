# 🔑 Points importants à connaître avec **Docker Compose V2**

### 1. 🚀 Commande unifiée

* Avant (V1) → `docker-compose up`
* Maintenant (V2) → `docker compose up` (intégré à Docker CLI).
  👉 Plus besoin d’installer un binaire séparé (`docker-compose`).

---

### 2. 🏷️ Version implicite du fichier

* Plus besoin de `version: "3.9"`.
* Tu écris directement `services:`, `networks:`, `volumes:`.
* Docker gère automatiquement les features disponibles selon ton moteur Docker.

---

### 3. 📂 Multi-profiles (`profiles`)

Tu peux définir des **profils** pour séparer dev/prod/test dans un seul `docker-compose.yml` :

```yaml
services:
  db:
    image: postgres:15
    profiles: ["dev"]   # ce service ne tourne qu’en dev
```

Et tu lances avec :

```bash
docker compose --profile dev up
```

---

### 4. 🔄 Dépendances et santé

* V2 permet de mieux gérer les dépendances avec `depends_on.condition: service_healthy`.
* Plus fiable que le simple `depends_on` (qui n’attendait pas que le service soit “prêt”).

---

### 5. 📦 Extensions (`x-…`)

Tu peux définir des blocs réutilisables avec `x-logging`, `x-healthcheck`, etc.
👉 Très pratique pour éviter de dupliquer du code.

Exemple :

```yaml
x-logging: &default-logging
  driver: json-file
  options:
    max-size: "10m"
    max-file: "3"

services:
  api:
    image: myapi
    logging: *default-logging
```

---

### 6. 🛡️ Sécurité et bonnes pratiques

* **Ne pas exposer inutilement de ports** (ex: Postgres en prod).
* **Supprimer `container_name`** → ça bloque le scaling (`--scale`).
* **Exécuter en non-root** → définis un utilisateur dans ton Dockerfile (`USER appuser`).
* **Limiter les permissions** → `read_only: true`, `cap_drop: [ALL]`, `security_opt: [no-new-privileges:true]`.

---

### 7. 📊 Observabilité

* Tu peux ajouter des **healthchecks** partout.
* Tu peux brancher des outils comme **Prometheus / Grafana / ELK** via Compose pour un monitoring local.

---

### 8. ⚡ Multi-fichiers

Avec V2, c’est beaucoup plus simple de gérer **plusieurs fichiers Compose** (ex: dev/prod/override) :

```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml up
```

Cela permet d’avoir :

* un `docker-compose.yml` **générique**,
* un `docker-compose.override.yml` pour le **dev**,
* un `docker-compose.prod.yml` pour la **prod**.

---

### 9. 📂 Organisation recommandée

Structure typique d’un projet pro :

```
project/
├─ docker-compose.yml        # config générique
├─ docker-compose.override.yml   # config dev
├─ docker-compose.prod.yml   # config prod
├─ nginx/
│   └─ default.conf
├─ .env
└─ app/
    ├─ Dockerfile
    ├─ requirements.txt
    └─ src/...
```



Très bonne question 👌

La commande :

```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml up
```

signifie :

---

## 🔎 Décomposition

* **`docker compose`** → tu utilises Docker Compose V2 (intégré à Docker).
* **`-f docker-compose.yml`** → tu précises un premier fichier (souvent le fichier de base).
* **`-f docker-compose.prod.yml`** → tu ajoutes un deuxième fichier qui va **surcharger ou compléter** le premier.
* **`up`** → démarre les conteneurs avec la configuration finale (après la fusion des fichiers).

---

## ⚡ Comment ça marche ?

Docker Compose **fusionne** les fichiers dans l’ordre où tu les passes :

1. Il lit `docker-compose.yml` → configuration par défaut (services, réseaux, volumes).
2. Il lit `docker-compose.prod.yml` → ce fichier peut **ajouter** ou **remplacer** certains paramètres.
3. Résultat = un seul fichier virtuel, qui est utilisé pour lancer les services.

👉 La **priorité est donnée au dernier fichier** (`docker-compose.prod.yml` dans ton cas).

---

## 📖 Exemple concret

### `docker-compose.yml` (base)

```yaml
services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DEBUG=True
```

### `docker-compose.prod.yml` (override prod)

```yaml
services:
  app:
    environment:
      - DEBUG=False
    ports:
      - "80:8000"   # override le port 8000:8000
```

### Résultat final quand tu fais la commande :

```yaml
services:
  app:
    build: .
    environment:
      - DEBUG=False
    ports:
      - "80:8000"
```

👉 Donc en **prod**, ton app tourne sur le port 80 et sans debug.

---

## 🎯 À retenir

* `-f` permet de **combiner plusieurs fichiers Compose**.
* L’ordre est **important** : le dernier fichier écrase les valeurs des précédents.
* Usage courant :

  * `docker-compose.yml` = base commune (dev + prod).
  * `docker-compose.override.yml` = config dev (volumes bind, ports ouverts, tty, etc.).
  * `docker-compose.prod.yml` = config prod (sécurité, pas de volumes, moins de ports, logs optimisés, etc.).





📦 Différence DEV vs PROD
🔹 En développement

On utilise souvent des bind mounts (.:/app) pour monter ton code directement dans le conteneur.

Avantage : toute modification locale est visible instantanément dans le conteneur → idéal pour coder.

Inconvénient : moins sécurisé, moins performant, dépend du système de fichiers de l’hôte.

👉 Exemple dev :

services:
  web:
    volumes:
      - .:/app

🔹 En production

Pas de bind mount du code → on ne monte pas .:/app.

Le code est déjà copié dans l’image Docker (via le Dockerfile → COPY . /app).

Résultat : l’image est autonome, portable, immuable → plus propre et fiable.

👉 Exemple prod :

services:
  web:
    image: mon-app:1.0.0   # le code est déjà dans l'image

📂 Cas particuliers où les volumes restent utiles en PROD

✅ Données persistantes

Ex : base de données (Postgres, MySQL, MongoDB).

Ici on utilise un volume nommé (postgres_data) pour stocker les données hors du conteneur, sinon elles disparaissent à chaque redémarrage.

services:
  database:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data
volumes:
  postgres_data:


✅ Logs / fichiers générés

Si ton app génère des fichiers (uploads, rapports, images, vidéos, etc.), tu peux :

utiliser un volume nommé (ex: uploads:/app/media),

ou mieux → uploader directement vers un stockage externe (S3, MinIO, etc.).

✅ Cache / sessions

Redis ou autre service peut utiliser un volume pour garder des données temporaires entre redémarrages.

🚫 Ce qu’on évite absolument en prod

❌ Monter le code source (.:/app) → dépend de la machine hôte, casse l’immutabilité.
❌ Monter les configs sensibles depuis l’hôte → on préfère env_file ou un gestionnaire de secrets.



# les options Docker Compose V2


### `--all-resources`

* **Ce que ça fait** : inclut **toutes** les ressources définies dans tes fichiers Compose (réseaux, volumes, configs, secrets…), **même si elles ne sont pas utilisées** par un service.
* **Quand l’utiliser** : surtout avec des commandes qui **convertissent** ou **inspectent** ta stack (ex. `convert`) pour voir l’intégralité de ce que décrit ta config.
* **Exemple** :

  ```bash
  docker compose convert --all-resources
  ```

  → Affiche la configuration complète (y compris réseaux/volumes non référencés).

---

### `--ansi auto`

* **Ce que ça fait** : contrôle l’affichage des **couleurs/formatages ANSI** dans la sortie.
* **Valeurs** : `never` (jamais), `always` (toujours), `auto` (par défaut, selon si la sortie est un terminal).
* **Quand l’utiliser** : pour des scripts CI/CD ou des logs où tu veux **désactiver** les caractères de contrôle.
* **Exemple** :

  ```bash
  docker compose --ansi never up
  ```

---

### `--compatibility`

* **Ce que ça fait** : active un **mode compatibilité** qui tente d’interpréter certains champs hérités (ex. `deploy:` de Swarm) et de les **adapter** au mode Compose classique quand c’est possible.
* **Quand l’utiliser** : si tu as des fichiers pensés pour **Swarm** (v3, `deploy.resources`, `deploy.replicas`, etc.) et que tu veux **en tirer parti** hors Swarm.
* **Remarque** : tout n’est pas transposable ; Compose fera au mieux (ex. limites CPU/mémoire).
* **Exemple** :

  ```bash
  docker compose --compatibility up -d
  ```

---

### `--dry-run`

* **Ce que ça fait** : exécute la commande en **mode simulation** (montre ce que Compose **ferait** sans réellement le faire).
* **Quand l’utiliser** : avant un `up`, `down`, `rm`, `pull`, etc., pour **prévisualiser** l’impact.
* **Exemple** :

  ```bash
  docker compose --dry-run up
  ```

---

### `--env-file <chemin>`

* **Ce que ça fait** : indique un **fichier d’environnement alternatif** (par défaut, Compose lit `.env` dans le répertoire du projet).
* **Quand l’utiliser** : pour **changer de contexte** (ex. `.env.prod`, `.env.staging`).
* **Exemple** :

  ```bash
  docker compose --env-file .env.prod up -d
  ```
* **Astuce** : ne pas confondre avec `env_file:` (clé YAML **dans** le service).

  * `--env-file` : global, résout les **variables** utilisées dans le compose (ex. `${POSTGRES_USER}`).
  * `env_file:` : injecte des variables **au service** au runtime.

---

### `-f, --file <fichier>`

* **Ce que ça fait** : précise **un ou plusieurs fichiers** Compose. Tu peux répéter `-f` pour **fusionner** des fichiers.
* **Règle de priorité** : **le dernier fichier** a la priorité (il **surcharge** les précédents).
* **Quand l’utiliser** : pour séparer **base/dev/prod**.
* **Exemple** :

  ```bash
  docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
  ```

---

### `--parallel <N>` (ex. `-1` = illimité)

* **Ce que ça fait** : contrôle le **degré de parallélisme** pour des actions sur plusieurs services (build, pull, push…).
* **Quand l’utiliser** : pour **accélérer** (ou limiter) les opérations lourdes sur plusieurs services.
* **Exemples** :

  ```bash
  docker compose pull --parallel 4      # télécharge 4 services en parallèle
  docker compose build --parallel -1    # parallélisme illimité
  ```

---

### `--profile <nom>`

* **Ce que ça fait** : **active** un ou plusieurs **profils** définis dans ton compose (clé `profiles:` au niveau des services).
* **Quand l’utiliser** : activer/désactiver des services selon les environnements (**dev**, **test**, **prod**, **ops**…).
* **Exemples** :

  ```bash
  docker compose --profile prod up -d
  docker compose --profile dev --profile metrics up
  ```

---

### `--progress <type>`

* **Ce que ça fait** : ajuste le **format d’affichage** pendant les opérations qui ont une progression (surtout `build`, parfois `pull/push`).
* **Valeurs** : `auto`, `tty` (barres jolies pour terminal), `plain` (texte brut), `json`, `quiet`.
* **Quand l’utiliser** : en **CI**, préfère `plain` ou `json`; en local, garde `auto`/`tty`.
* **Exemples** :

  ```bash
  docker compose build --progress=plain
  docker compose build --progress=json
  ```

---

### `--project-directory <dossier>`

* **Ce que ça fait** : définit le **répertoire de travail** du projet (d’où Compose résout `.env`, chemins relatifs, etc.).
* **Valeur par défaut** : le **répertoire du premier fichier** passé avec `-f`.
* **Quand l’utiliser** : si tes fichiers sont **ailleurs** ou que tu lances la commande depuis un autre dossier.
* **Exemple** :

  ```bash
  docker compose --project-directory ./deploy -f ./deploy/compose.yml up
  ```

---

### `-p, --project-name <nom>`

* **Ce que ça fait** : **nomme explicitement** le projet. Compose l’utilise comme **préfixe** pour nommer conteneurs, réseaux, volumes (`<projet>_<service>_1`).
* **Quand l’utiliser** : pour **éviter les collisions** entre stacks similaires, ou pour aligner le **naming** avec tes conventions.
* **Exemples** :

  ```bash
  docker compose -p erp-prod up -d
  docker compose -p blog-staging -f docker-compose.yml -f docker-compose.staging.yml up
  ```

---

## Exemples combinés (scénarios courants)

**1) Démarrer la prod avec un autre `.env`, nom de projet et sortie “plain”**

```bash
docker compose \
  -p myapp-prod \
  --env-file .env.prod \
  -f docker-compose.yml -f docker-compose.prod.yml \
  --compatibility \
  up -d
```

**2) Builder en CI (sortie JSON, parallélisme limité)**

```bash
docker compose \
  --progress=json \
  --ansi=never \
  build --parallel 4
```

**3) Prévisualiser l’impact d’un `down`**

```bash
docker compose --dry-run down
```


# Utiliser `-f` pour préciser un ou plusieurs fichiers Compose

## 1) Un seul fichier

* **But** : indiquer un fichier `compose.yaml` qui n’est pas dans le dossier courant.

* **Commande** :

  ```bash
  docker compose -f ~/sandbox/rails/compose.yaml pull db
  ```

  → Ici, on **tire** l’image du service `db` en se basant sur le fichier indiqué.

* **Alternative** : variable d’environnement

  ```bash
  export COMPOSE_FILE=~/sandbox/rails/compose.yaml
  docker compose pull db
  ```

  > ⚠️ Si tu passes `-f` en ligne de commande, il **prime** sur `COMPOSE_FILE`.

## 2) Plusieurs fichiers (merge/overlay)

* **But** : combiner **plusieurs** fichiers Compose. Le résultat final = **fusion** dans l’ordre où tu les fournis. **Le dernier** fichier **écrase** (override) les champs identiques et **ajoute** les nouveaux.

* **Commande** :

  ```bash
  docker compose -f compose.yaml -f compose.admin.yaml run backup_db
  ```

* **Exemple de fusion**

  * `compose.yaml` :

    ```yaml
    services:
      webapp:
        image: examples/web
        ports:
          - "8000:8000"
        volumes:
          - "/data"
    ```
  * `compose.admin.yaml` :

    ```yaml
    services:
      webapp:
        build: .
        environment:
          - DEBUG=1
    ```
  * **Résultat effectif** : `webapp` hérite de `image/ports/volumes` **+** override/ajout `build` et `environment`.

* **Chemins relatifs** : avec plusieurs `-f`, **tous les chemins** (volumes, includes…) sont **relatifs au premier fichier** fourni. Tu peux changer cette base avec `--project-directory`.

## 3) Lire depuis `stdin`

* **But** : alimenter Compose depuis un pipe.
* **Commande** :

  ```bash
  cat compose.generated.yaml | docker compose -f - config
  ```

  > Avec `-f -`, **tous les chemins** sont relatifs au **répertoire courant**.

## 4) Sans `-f` (auto-détection)

* Si tu ne passes pas `-f`, Compose remonte l’arborescence à partir du dossier courant à la recherche de **`compose.yaml`** (recommandé) ou **`docker-compose.yaml`**.

---

# Spécifier un nom de projet avec `-p`

Chaque stack Compose a un **nom de projet**. Il sert de **préfixe** pour les conteneurs, réseaux, volumes (ex. `monprojet_web_1`).

## Ordre de priorité (du plus fort au plus faible)

1. `-p, --project-name` sur la **ligne de commande**
2. Variable d’env `COMPOSE_PROJECT_NAME`
3. Clé `name:` (top-level) **dans** le fichier Compose (ou le **dernier** des fichiers `-f`)
4. **Nom du dossier** qui contient le (premier) fichier Compose
5. **Dossier courant** si aucun fichier n’est spécifié

> **Contrainte** : noms autorisés = minuscules, chiffres, tirets, underscores. S’il y a des majuscules/espaces dans le nom du dossier, utilise `-p`.

## Exemples

```bash
docker compose -p my_project ps -a
docker compose -p my_project logs
```

Sortie typique :

```
NAME                 SERVICE    STATUS     PORTS
my_project_demo_1    demo       running
```

---

# Activer des services optionnels avec les **profils**

* **But** : activer certains services **seulement** quand un profil est présent.
* **Définition dans YAML** :

  ```yaml
  services:
    metrics:
      image: prom/prometheus
      profiles: ["metrics"]
  ```
* **Activer un ou plusieurs profils** :

  ```bash
  docker compose --profile metrics up -d
  docker compose --profile frontend --profile debug up
  ```
* **Variable d’env** : `COMPOSE_PROFILES=frontend,debug`

> Sans profil explicitement activé, **les services sans `profiles:`** démarrent normalement, et **ceux qui ont `profiles:`** sont **ignorés**.

---

# Contrôler le **parallélisme**

* **But** : limiter/augmenter le nombre d’opérations parallèles (build/pull/push…).
* **Commande** :

  ```bash
  docker compose --parallel 1 pull     # tire les images une par une
  docker compose --parallel 4 build    # build jusqu’à 4 services en parallèle
  docker compose --parallel -1 pull    # illimité
  ```
* **Variable d’env** : `COMPOSE_PARALLEL_LIMIT`

---

# Variables d’environnement utiles (équivalents aux flags)

* `COMPOSE_FILE` ⇔ `-f`
* `COMPOSE_PROJECT_NAME` ⇔ `-p`
* `COMPOSE_PROFILES` ⇔ `--profile`
* `COMPOSE_PARALLEL_LIMIT` ⇔ `--parallel`
* `COMPOSE_IGNORE_ORPHANS=true` : désactive la détection des **orphelins** (conteneurs de l’ancien projet non définis dans la config actuelle).
* `COMPOSE_MENU=false` : désactive le **menu d’aide** en mode attaché (équivaut à `--menu=false` avec `up`).

> ⚠️ Si tu donnes **le flag en CLI**, il **écrase** la variable d’environnement correspondante.

---

# **Dry Run** (`--dry-run`) pour tester sans changer l’état

* **But** : voir **exactement** ce que Compose ferait (pull/build/create/start/stop…) **sans rien exécuter**.
* **Commande** :

  ```bash
  docker compose --dry-run up --build -d
  ```
* **Interprétation** : tu verras le **plan d’exécution** (images tirées, services créés, ordre de démarrage, attente des `healthcheck`, etc.).
* **Limite** : ne s’applique pas aux commandes **purement informatives** (`ps`, `ls`, `logs`…).

---

# Sous-commandes courantes (avec mini-exemples)

| Commande  | À quoi ça sert                                         | Exemple utile                                                          |
| --------- | ------------------------------------------------------ | ---------------------------------------------------------------------- |
| `alpha`   | commandes expérimentales                               | —                                                                      |
| `attach`  | attacher STDIN/STDOUT/STDERR à un conteneur de service | `docker compose attach api`                                            |
| `bridge`  | convertir des fichiers compose vers un autre modèle    | —                                                                      |
| `build`   | (re)construire les images                              | `docker compose build --no-cache api`                                  |
| `config`  | résoudre et afficher la config **finale**              | `docker compose -f a.yml -f b.yml config`                              |
| `cp`      | copier fichiers entre hôte et conteneur                | `docker compose cp api:/app/logs ./logs`                               |
| `create`  | **créer** les conteneurs (sans démarrer)               | `docker compose create`                                                |
| `down`    | arrêter et **supprimer** conteneurs + réseaux          | `docker compose down -v` (supprime aussi les volumes nommés du projet) |
| `events`  | flux d’événements en temps réel                        | `docker compose events`                                                |
| `exec`    | exécuter une commande **dans** un conteneur            | `docker compose exec api sh`                                           |
| `images`  | lister les images utilisées                            | `docker compose images`                                                |
| `kill`    | kill (SIGKILL) des services                            | `docker compose kill api`                                              |
| `logs`    | voir les logs                                          | `docker compose logs -f api`                                           |
| `ls`      | lister les projets compose actifs                      | `docker compose ls`                                                    |
| `pause`   | mettre en pause (SIGSTOP)                              | `docker compose pause api`                                             |
| `port`    | afficher le port publié d’un service                   | `docker compose port web 80`                                           |
| `ps`      | lister les conteneurs du projet                        | `docker compose ps -a`                                                 |
| `publish` | publier l’application compose (cas avancés)            | —                                                                      |
| `pull`    | tirer les images                                       | `docker compose pull`                                                  |
| `push`    | pousser les images                                     | `docker compose push`                                                  |
| `restart` | redémarrer conteneurs                                  | `docker compose restart api`                                           |
| `rm`      | supprimer conteneurs **arrêtés**                       | `docker compose rm`                                                    |
| `run`     | lancer une commande “one-off”                          | `docker compose run --rm api python manage.py migrate`                 |
| `start`   | démarrer services **déjà créés**                       | `docker compose start`                                                 |
| `stop`    | arrêter services                                       | `docker compose stop`                                                  |
| `top`     | process en cours dans les conteneurs                   | `docker compose top`                                                   |
| `unpause` | reprendre des services pausés                          | `docker compose unpause api`                                           |
| `up`      | **créer + démarrer** (ou recréer)                      | `docker compose up -d --build`                                         |
| `version` | afficher la version de Compose                         | `docker compose version`                                               |
| `volumes` | lister les volumes du projet                           | `docker compose volumes`                                               |
| `wait`    | bloquer jusqu’à l’arrêt des services                   | `docker compose wait`                                                  |
| `watch`   | rebuild/refresh quand des fichiers changent (dev)      | `docker compose watch`                                                 |

---

## Récap express

* `-f` : combine des fichiers (le **dernier** a priorité). Chemins relatifs → **premier fichier**.
* `-p` : fixe le **nom de projet** (évite collisions).
* `--profile` : active des **services optionnels**.
* `--parallel` : contrôle la **concurrence** (build/pull).
* Variables d’env équivalentes (`COMPOSE_*`) existent, mais **les flags CLI gagnent**.
* `--dry-run` : montre **exactement** ce que Compose ferait, **sans effet de bord**.
