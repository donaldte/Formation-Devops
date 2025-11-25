# Qu’est-ce que `.dockerignore` ?

C’est un fichier placé **à la racine du *build context*** (le dossier que tu passes à `docker build` ou `build.context` dans Compose) qui **exclut des fichiers/dossiers** lors de l’envoi du contexte au moteur Docker.
But = **builds plus rapides**, **caches plus stables**, **images plus petites**, et **zéro fuite de secrets**.

> Important : si un fichier est ignoré par `.dockerignore`, il **n’est pas disponible** pour `ADD`/`COPY` pendant le build (sauf si tu le “ré-inclues” avec `!`).

---

# Règles et syntaxe (comme `.gitignore`)

* Une ligne = un motif (glob) : `*.log`, `cache/`, `**/node_modules`
* `#` = commentaire
* `!motif` = **ré-inclut** ce qui a été exclu avant
* **Dernière règle qui matche gagne** (ordre important)
* Le fichier doit s’appeler **`.dockerignore`** et être **au root du contexte**.

---

# Quand l’utiliser ?

* Tu fais `COPY . /app` (classique) → **exclus** tout ce qui est inutile (git, caches, gros fichiers, secrets).
* Tu veux **accélérer** le build et **mieux profiter du cache** (moins de “bruit”).
* Tu veux **éviter d’envoyer** des secrets (.env, clés, certificats) ou des données (ex. `media/`, `pgdata/`).

---

# Exemples prêts à l’emploi

## 1) Backend Python/Django

```dockerignore
# VCS
.git
.gitignore

# Python
__pycache__/
*.pyc
*.pyo
*.pyd
*.pytest_cache/
.mypy_cache/
.venv/
venv/

# Django
staticfiles/
media/

# Outils / IDE
*.sqlite3
*.swp
.DS_Store
.vscode/
.idea/

# Logs & artefacts
*.log
coverage/
dist/
build/

# Secrets (ne jamais copier dans l'image)
.env
*.pem
*.key
*.crt

# Conteneurs / DB locales
docker/
pgdata/
```

## 2) Frontend Node/React/Vite

```dockerignore
# VCS
.git
.gitignore

# Node
node_modules/
npm-debug.log*
yarn-error.log*
pnpm-lock.yaml # ⚠️ Garde le lockfile si tu l'utilises !
# (Conseil: ne PAS ignorer le lockfile de TON gestionnaire)

# Build output
dist/
build/
.cache/
.tmp/

# IDE / OS
.DS_Store
.vscode/
.idea/

# Secrets
.env
.env.*
```

> Astuce Node : dans le Dockerfile, fais `COPY package*.json .` puis `npm ci`, puis **après** seulement `COPY . .`. Et garde **le lockfile** (npm, yarn ou pnpm) — n’ignore pas celui que tu utilises.

---

# Patterns utiles (rappels)

```dockerignore
# ignorer tout dans secrets/, sauf public.key
secrets/*
!secrets/public.key

# ignorer tous les .log partout
**/*.log

# ignorer un gros dossier de données locales
data/
```

---

# Bonnes pratiques (pro)

* **Réduis le contexte** : mets `build.context` au plus proche du code à copier.
* **Ne copie pas toute la racine** si tu peux faire `COPY src/ /app/src/` (plus ciblé).
* **Verrouille les secrets** : `.env`, clés SSH, dossiers `.aws/`, etc. → **toujours** ignorés.
* **Optimise le cache** : ordonne ton Dockerfile pour que les étapes stables (install deps) ne soient pas invalidées par des fichiers qui changent souvent.
* **Vérifie la taille du contexte** :

  * Builder classique : “Sending build context to Docker daemon **XX MB**”
  * BuildKit : “transferring context: **YY MB**”
* **Compose** : `.dockerignore` s’applique **au dossier `build.context`** :

  ```yaml
  services:
    web:
      build:
        context: .
        dockerfile: Dockerfile
  ```

---

# Mini-exemple : Dockerfile Python optimisé

```dockerfile
# syntax=docker/dockerfile:1
FROM python:3.12-slim AS base
WORKDIR /app

# Étape deps (cache stable)
COPY pyproject.toml poetry.lock ./
RUN pip install --no-cache-dir poetry && poetry export -f requirements.txt | pip install -r /dev/stdin

# Étape code
COPY . .   # Grâce au .dockerignore, tu ne copies que l’utile
CMD ["gunicorn", "myapp.wsgi:application", "-b", "0.0.0.0:8000"]
```


