# Mini-cours : **Extensions `x-`** dans Docker Compose

Les **extensions** sont des blocs YAML dont la clé commence par **`x-`** (ex. `x-logging`, `x-service-base`). Elles servent à **modulariser** et **réutiliser** de la configuration.
Compose **ignore** ces clés `x-` (c’est l’unique cas où des champs inconnus sont ignorés), mais tu peux **référencer leur contenu** via **ancres & alias**.

---

## Règles rapides

* **Déclaration** : au **niveau racine** du fichier (top-level) avec un préfixe `x-`.
* **Contenu** : n’importe quel YAML (maps, listes, scalaires).
* **Utilisation** : combine avec **ancres (`&`)** et **alias (`*`)** pour injecter le contenu dans tes services (souvent avec la **fusion de map** `<<:`).
* **Multi-fichiers** : les **ancres ne traversent pas** les fichiers `-f`. Si tu as plusieurs compose, **redéclare** tes ancres/`x-` dans chaque fichier où tu en as besoin.
* **Validation** : `docker compose config` montre le rendu final (les `x-` n’y figurent pas, mais leurs **valeurs injectées** oui).

---

## Exemple minimal

```yaml
# ----- Extensions réutilisables (ignorées par Compose) -----
x-logging: &logging
  driver: json-file
  options: { max-size: "10m", max-file: "3" }

x-healthcheck-http: &hc_http
  test: ["CMD-SHELL", "curl -fsS http://localhost:8000/healthz || exit 1"]
  interval: 10s
  timeout: 3s
  retries: 5
  start_period: 15s

x-service-base: &svc_base
  restart: unless-stopped
  logging: *logging
  environment:
    TZ: "UTC"
    LANG: "C.UTF-8"
  networks: [app_net]

# ----- Définition réseau -----
networks:
  app_net: {}

# ----- Services qui réutilisent les fragments -----
services:
  web:
    <<: *svc_base                 # hérite du bloc commun
    image: myorg/web:1.2.3
    healthcheck: *hc_http
    ports: ["80:8000"]

  worker:
    <<: *svc_base
    image: myorg/worker:1.2.3
    command: python worker.py
    environment:
      WORKER_CONCURRENCY: "4"

  db:
    image: postgres:15.6
    <<: *svc_base                 # on peut aussi réutiliser en partie
    environment:
      POSTGRES_DB: app
      POSTGRES_USER: app
      POSTGRES_PASSWORD: secret
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata: {}
```

**Ce que ça t’apporte :**

* Une **seule source de vérité** pour les logs, variables communes, réseaux, etc.
* Des services plus **courts**, **cohérents**, et **faciles à maintenir**.
* Tu changes, par ex., la rotation de logs **à un seul endroit** (`x-logging`).

---

## Variante : listes réutilisées

```yaml
x-common-ports: &ports_http ["80:8000"]
x-common-vols:  &code_vols  ["./data:/data:rw"]

services:
  web:
    image: my/web
    ports:  *ports_http
    volumes: *code_vols

  admin:
    image: my/admin
    ports:  *ports_http
```

> ⚠️ Les **listes ne se fusionnent pas** : si tu dois “ajouter” un port, redéclare la liste ou crée une **seconde extension** (ex. `x-ports-http-admin`).

---

## Overlay dev/prod (multi-fichiers)

**Base** `compose.yaml` :

```yaml
x-service-base: &svc_base
  restart: unless-stopped
  logging:
    driver: json-file
    options: { max-size: "10m", max-file: "3" }

services:
  web:
    <<: *svc_base
    image: myorg/web:1.2.3
```

**Prod** `compose.prod.yaml` :

```yaml
# Redéclare (si besoin) et/ou surcharge
x-service-base: &svc_base
  restart: unless-stopped
  environment:
    APP_ENV: "production"

services:
  web:
    <<: *svc_base
    image: myorg/web:1.2.3
    deploy:  # (si tu utilises --compatibility)
      resources:
        limits:
          cpus: "1.0"
          memory: "512M"
```

Lance :

```bash
docker compose -f compose.yaml -f compose.prod.yaml up -d
```

---

## Bonnes pratiques & pièges

* ✅ Donne des **noms clairs** : `x-logging`, `x-healthcheck-http`, `x-service-base`, `x-labels-security`, etc.
* ✅ Utilise `<<: *ancre` pour **fusionner** des maps (héritage simple).
* ✅ Valide toujours avec `docker compose config`.
* ❌ N’attends pas que les **ancres voyagent entre fichiers** : elles sont **locales** au fichier YAML.
* ❌ N’abuse pas des `x-` : 3-5 blocs bien pensés > 15 fragments illisibles.


