# Include

1. **Plusieurs fichiers Compose** combinés avec `-f` (overlay/merge)
2. **`extends`** (hériter d’un service défini dans un autre fichier)
3. **Extensions `x-` + ancres/alias YAML** (fragments réutilisables dans un fichier)
4. **Fichiers externes** (env, configs, secrets) référencés par Compose

Voici un mini-cours clair, avec exemples.

---

# 1) “Include” par **plusieurs fichiers** (`-f`)

Tu fusionnes plusieurs fichiers pour composer ta stack. Le **dernier** fichier a **priorité** (il surcharge/ajoute).

```bash
# Base + prod : prod surchage la base
docker compose -f compose.yml -f compose.prod.yml up -d
```

**Règles clés**

* Les fichiers sont **fusionnés dans l’ordre**.
* **Listes** (ex: `ports`, `command`) → en général **remplacées** (pas fusionnées).
* **Maps** (ex: `environment`, `labels`) → **fusionnées** (les clés du dernier fichier gagnent).
* Tous les **chemins relatifs** sont résolus **par rapport au 1er fichier** donné à `-f`.
  (Tu peux changer la base avec `--project-directory`.)

**Exemple**
`compose.yml`

```yaml
services:
  web:
    image: my/web:1.0
    ports: ["8080:8080"]
```

`compose.prod.yml`

```yaml
services:
  web:
    image: my/web:1.0
    ports: ["80:8080"]         # remplace la liste
    environment:
      APP_ENV: "production"    # ajoute/fusionne
```

---

# 2) “Include” avec **`extends`** (hériter d’un service d’un autre fichier)

`extends` permet de **réutiliser** la config d’un service défini ailleurs (même fichier ou **autre fichier**), puis de **surcharger** localement.

`compose.base.yml`

```yaml
services:
  app_base:                      # service "modèle"
    image: my/app:1.2.3
    restart: unless-stopped
    environment:
      TZ: "UTC"
    networks: [app_net]
    # Empêche son démarrage par défaut :
    profiles: ["_base"]

networks:
  app_net: {}
```

`compose.dev.yml`

```yaml
services:
  app:
    extends:
      file: compose.base.yml     # chemin relatif au fichier courant
      service: app_base
    environment:
      APP_ENV: "development"
    ports: ["8000:8000"]
    volumes:
      - .:/app

networks:
  app_net: {}
```

Commande :

```bash
docker compose -f compose.base.yml -f compose.dev.yml up
```

**À savoir**

* `extends` **merge** d’abord la config héritée, puis **tes clés locales gagnent**.
* Les **chemins** (ex: `build.context`, `volumes`) du service **étendu** sont résolus **par rapport au fichier où ils sont déclarés** (celui pointé par `file:`).
* Astuce : mets `profiles: ["_base"]` sur les services-modèles pour éviter qu’ils ne démarrent.

Quand choisir `extends` plutôt que `-f` ?

* Quand tu veux **factoriser** des services “modèles” (base commune) et **choisir** explicitement qui hérite de quoi.
* Avec `-f`, tu fais un overlay global ; avec `extends`, tu **hérites service par service**.

---

# 3) “Include” interne avec **extensions `x-` + ancres/alias YAML**

C’est un **include intra-fichier** (pas entre fichiers) : tu déclares des blocs réutilisables puis tu les injectes.

```yaml
# Fragments réutilisables (ignored par Compose)
x-logging: &logging
  driver: json-file
  options: { max-size: "10m", max-file: "3" }

x-svc-base: &svc_base
  restart: unless-stopped
  logging: *logging
  environment:
    TZ: "UTC"

services:
  api:
    <<: *svc_base           # fusion de map (héritage)
    image: my/api:1.0
    ports: ["80:8080"]

  worker:
    <<: *svc_base
    image: my/worker:1.0
    command: python worker.py
```

**Rappels**

* `x-...` : sections **ignorées** par Compose (seule exception où des clés inconnues sont OK).
* `&nom` (ancre) / `*nom` (alias) / `<<: *nom` (fusion de map).
* ⚠️ Les **ancres/alias ne traversent pas les fichiers** → ils ne sont valables **que dans le YAML où ils sont déclarés**. Pour du cross-file, utilise plutôt `extends` ou `-f`.

---

# 4) “Inclure” des **fichiers externes** (env, configs, secrets)

Compose sait référencer des fichiers “auxiliaires”.

* **Variables d’environnement** globales au projet :
  `docker compose --env-file .env.prod up`
  (ou top-level `env_file:` **par service**)
* **Secrets**/**configs** (utile surtout en Swarm, mais support Compose existe) :

```yaml
secrets:
  db_password:
    file: ./secrets/db_password.txt

services:
  db:
    image: postgres
    secrets: [db_password]
```

---

## Bonnes pratiques “include”

* **Structure** : garde un `compose.yml` **base**, puis des overlays `compose.dev.yml`, `compose.prod.yml`.
* **Paths** : souviens-toi que les **chemins relatifs** (volumes, etc.) se basent sur le **1er** fichier passé à `-f`.
* **Listes vs maps** : saisis les **règles de merge** (listes remplacées, maps fusionnées).
* **Valide** ce que Compose va vraiment lancer :

  ```bash
  docker compose -f compose.yml -f compose.prod.yml config
  ```
* **Ne sur-multiplie pas** les fichiers : 2-3 suffisent dans 90% des cas.
* **`extends`** pour **hériter** de services “modèles” (et empêcher leur démarrage avec `profiles`).
* **`x-` + ancres** pour **factoriser** dans un même fichier (logs, healthcheck, base commune).

---

## Choisir la bonne approche

| Besoin                                         | Solution                                        |
| ---------------------------------------------- | ----------------------------------------------- |
| Avoir une base et des variantes (dev/prod)     | Multi-fichiers avec `-f`                        |
| Réutiliser un service “modèle” défini ailleurs | `extends` (service → service)                   |
| Factoriser des blocs communs dans un fichier   | `x-` + ancres/alias YAML                        |
| Charger des variables/fichiers externes        | `--env-file`, `env_file:`, `secrets`, `configs` |

