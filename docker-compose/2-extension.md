# 🎓 **Cours complet sur les extensions de fichiers dans Docker Compose (multi-fichiers)**

---

## 🚀 1️⃣ Qu’est-ce qu’une extension de fichier Compose ?

Docker Compose te permet de **diviser ta configuration** en plusieurs fichiers :

* un **fichier de base** (`docker-compose.yml`)
* un ou plusieurs **fichiers d’extension** (`docker-compose.dev.yml`, `docker-compose.prod.yml`, etc.)

👉 Ces fichiers peuvent **s’étendre**, **s’écraser** ou **ajouter** des paramètres.

Cela permet d’avoir :

* un seul fichier de base commun à tout le monde,
* et plusieurs variantes selon l’environnement (développement, production, staging…).

---

## ⚙️ 2️⃣ Principe

Imagine que tu as :

```
docker-compose.yml        # base commune
docker-compose.dev.yml    # version développement
docker-compose.prod.yml   # version production
```

Tu peux les combiner avec la commande :

```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml up
```

ou

```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

👉 Docker Compose **fusionne** ces fichiers dans l’ordre :

* le second **écrase ou complète** le premier,
* le troisième écrase les deux premiers, etc.

---

## 🧱 3️⃣ Exemple concret

### 🧩 **docker-compose.yml** (base commune)

```yaml
services:
  app:
    image: python:3.12-slim
    command: python -m http.server 8000
    expose:
      - "8000"
```

---

### 🧩 **docker-compose.dev.yml** (extension développement)

```yaml
services:
  app:
    ports:
      - "8000:8000"
    volumes:
      - ./app:/app
    command: python -m http.server 8000
```

---

### 🧩 **docker-compose.prod.yml** (extension production)

```yaml
services:
  app:
    command: gunicorn app.main:app --bind 0.0.0.0:8000
    deploy:
      resources:
        limits:
          cpus: "0.50"
          memory: 512M
```

---

### 🧠 En pratique

#### Pour le développement :

```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml up
```

> 🔹 Ports exposés pour ton navigateur
> 🔹 Montage du code local (volume)
> 🔹 Hot reload activé

#### Pour la production :

```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

> 🔹 Pas de port public direct
> 🔹 Ressources limitées
> 🔹 Commande adaptée à la prod (Gunicorn, etc.)

---

## ⚡ 4️⃣ Fusion logique entre fichiers

Quand Docker Compose fusionne les fichiers, il suit des règles précises :

| Type d’élément                            | Comportement                                  |
| ----------------------------------------- | --------------------------------------------- |
| **Clés simples** (ex: `image`, `command`) | La dernière valeur **remplace** la précédente |
| **Listes** (ex: `ports`, `volumes`)       | Les valeurs sont **ajoutées** (concatenées)   |
| **Objets** (ex: `environment`, `deploy`)  | Les valeurs sont **fusionnées clé par clé**   |

---

### 🧩 Exemple de fusion

Base :

```yaml
services:
  web:
    image: nginx
    ports:
      - "80:80"
```

Override :

```yaml
services:
  web:
    ports:
      - "8080:80"
    environment:
      - MODE=prod
```

Résultat fusionné :

```yaml
services:
  web:
    image: nginx
    ports:
      - "80:80"
      - "8080:80"
    environment:
      - MODE=prod
```

---

## 📁 5️⃣ Bonnes pratiques professionnelles

| Bonne pratique                                                | Description                                                                             |
| ------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| ✅ **Nommer clairement** tes fichiers                          | `docker-compose.dev.yml`, `docker-compose.prod.yml`, `docker-compose.staging.yml`, etc. |
| ✅ **Toujours garder un fichier `docker-compose.yml` de base** | Contient les définitions communes à tous les environnements                             |
| ✅ **Ne jamais mélanger dev et prod dans un seul fichier**     | Risque d’erreurs ou d’exposition de ports                                               |
| ✅ **Toujours spécifier l’ordre avec `-f`**                    | L’ordre compte ! (le dernier écrase les précédents)                                     |
| ✅ **Utiliser un `.env` séparé**                               | Pour gérer les variables selon l’environnement                                          |
| ✅ **Utiliser des fichiers d’override distincts**              | Permet d’ajouter des services spécifiques (ex: monitoring, redis, etc.)                 |

---

## 🧠 6️⃣ Exemple professionnel complet (dev/prod)

### 📁 Structure

```
/home/ubuntu/app1/
├── docker-compose.yml
├── docker-compose.dev.yml
├── docker-compose.prod.yml
├── .env
└── backend/
    ├── Dockerfile
    ├── requirements.txt
    └── app/main.py
```

---

### **docker-compose.yml** (base)

```yaml
services:
  backend:
    build: ./backend
    expose:
      - "8000"
    environment:
      - TZ=UTC
    restart: unless-stopped
```

---

### **docker-compose.dev.yml**

```yaml
services:
  backend:
    ports:
      - "8000:8000"
    volumes:
      - ./backend:/app
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

---

### **docker-compose.prod.yml**

```yaml
services:
  backend:
    command: gunicorn app.main:app --bind 0.0.0.0:8000 --workers 3
    deploy:
      resources:
        limits:
          cpus: "0.50"
          memory: 512M
```

---

### 🔧 Commandes

* En **dev local** :

  ```bash
  docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build
  ```
* En **prod sur EC2** :

  ```bash
  docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
  ```

---

## 🧩 7️⃣ En résumé

| Concept       | Exemple                   | Rôle                  |
| ------------- | ------------------------- | --------------------- |
| **Base**      | `docker-compose.yml`      | Fichier commun        |
| **Extension** | `docker-compose.dev.yml`  | Fichier pour dev      |
| **Extension** | `docker-compose.prod.yml` | Fichier pour prod     |
| **Fusion**    | `-f base -f extension`    | Combine les deux      |
| **Priorité**  | dernier fichier           | Écrase les précédents |

---

## 💡 8️⃣ Combiner avec les *extensions YAML (x-...)*

Les **fichiers étendus (`-f`)** et les **extensions YAML (`x-...`)** sont **complémentaires** :

Tu peux très bien avoir :

```yaml
# docker-compose.yml
x-resource-limits: &resources
  deploy:
    resources:
      limits:
        cpus: "0.5"
        memory: 512M

services:
  backend:
    image: myapp/backend
    <<: *resources
```

Puis dans `docker-compose.prod.yml` :

```yaml
services:
  backend:
    command: gunicorn app.main:app --bind 0.0.0.0:8000 --workers 3
```

👉 Tu obtiens ainsi un **setup ultra-propre** :

* les **extensions YAML** centralisent les règles communes,
* les **extensions de fichiers** gèrent les environnements.

