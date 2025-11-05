# Mini-cours : Fragments YAML (ancres & alias) pour Docker Compose

Les **fragments** YAML (aussi appelés *ancres* et *alias*) te permettent de **réutiliser des blocs** de configuration dans ton `compose.yaml`. C’est 100% YAML (pas spécifique à Compose) et ça évite les copier-coller, donc **moins d’erreurs** et un fichier **plus court**.

---

## Pourquoi / quand s’en servir ?

* Plusieurs services partagent les **mêmes options** (logs, healthcheck, réseaux, variables).
* Tu veux **centraliser** un réglage (taille des logs, politique de restart) et le **changer à un seul endroit**.
* Tu veux **factoriser** des listes (ports, volumes) ou des maps (environment).

---

## Syntaxe de base

* **Ancre** : `&nom` — elle **déclare** un bloc réutilisable.
* **Alias** : `*nom` — il **réfère** au bloc ancré.
* **Fusion de maps** : `<<: *nom` — **injecte** une map (objet) ancrée dans la map courante.

```yaml
x-logging: &logging   # ancre un bloc "logging"
  driver: json-file
  options:
    max-size: "10m"
    max-file: "3"

services:
  api:
    logging: *logging  # réutilise le bloc via alias
```

> Rappels : pas d’espace entre `&`/`*` et le nom. Les ancres peuvent s’appliquer à **n’importe quel nœud** YAML : map (objet), liste, valeur simple.

---

## Fusionner des objets avec `<<`

`<<: *ancre` **merge** une map dans une autre. Pratique pour des “bases” communes.

```yaml
x-service-base: &service_base
  restart: unless-stopped
  networks: [app_net]
  environment:
    TZ: "UTC"
    APP_ENV: "production"

services:
  web:
    <<: *service_base       # injecte les clés/valeurs de service_base
    image: my/web:1.0.0
    ports: ["80:8080"]      # clés ajoutées / surchargées après la fusion

  worker:
    <<: *service_base
    image: my/worker:1.0.0
    command: python worker.py
```

---

## Réutiliser des **listes**

Tu peux ancrer une **liste** (ports, volumes…) et la réutiliser telle quelle (mais **on ne “merge” pas** les listes ; on les **remplace**).

```yaml
x-common-ports: &ports_http ["80:8080"]
x-common-vols: &code_vols ["./.data:/data:rw"]

services:
  web:
    image: my/web
    ports: *ports_http
    volumes: *code_vols

  admin:
    image: my/admin
    ports: *ports_http    # réutilise la même liste
```

Si tu dois **ajouter** un élément à une liste réutilisée, redéclare la liste en entier ou crée une **deuxième ancre**.

---

## Exemple complet, prêt à copier

```yaml
# Blocs "extension" ignorés par Compose pour les services,
# mais parfaits pour ancrer du réutilisable.
x-logging: &logging
  driver: json-file
  options:
    max-size: "10m"
    max-file: "3"

x-healthcheck-http: &hc_http
  test: ["CMD-SHELL", "curl -fsS http://localhost:8000/healthz || exit 1"]
  interval: 10s
  timeout: 3s
  retries: 5
  start_period: 15s

x-service-base: &svc_base
  restart: unless-stopped
  networks: [app_net]
  logging: *logging
  environment:
    TZ: "UTC"
    LANG: "C.UTF-8"

networks:
  app_net: {}

services:
  web:
    <<: *svc_base               # hérite du bloc commun
    image: myorg/web:1.2.3
    depends_on:
      db:
        condition: service_healthy
    healthcheck: *hc_http       # réutilise un healthcheck ancré
    ports: ["80:8000"]

  worker:
    <<: *svc_base
    image: myorg/worker:1.2.3
    command: python worker.py
    # Peut surcharger/ajouter :
    environment:
      <<: *{ }                  # (astuce : si tu avais une map ancrée ici)
      WORKER_CONCURRENCY: "4"

  db:
    image: postgres:15.6
    restart: unless-stopped
    networks: [app_net]
    logging: *logging
    environment:
      POSTGRES_DB: app
      POSTGRES_USER: app
      POSTGRES_PASSWORD: secret
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U $$POSTGRES_USER -d $$POSTGRES_DB -h localhost"]
      interval: 10s
      timeout: 5s
      retries: 10
      start_period: 20s

volumes:
  pgdata: {}
```

> 💡 **Validation** : visualise le rendu final (après ancres/alias/fusions) avec :
> `docker compose config`
> (très utile pour “voir” ce que Compose comprend réellement).

---

## Limites & pièges à éviter

* **Ancres ≠ cross-file** : les ancres **ne traversent pas** les **fichiers `-f` différents**. Chaque fichier est un document YAML **indépendant**. Si tu utilises plusieurs fichiers, définis les ancres **dans chaque** fichier où tu en as besoin.
* **Listes non fusionnées** : `<<` **ne fusionne pas** les listes (ports, volumes…). Tu dois **réassigner** la liste complète ou **ancrer plusieurs variantes**.
* **Surcharges** : les clés **déclarées après** un `<<` **écrasent** celles fusionnées (pratique pour customiser par service).
* **Lisibilité** : n’abuse pas des ancres. Préfère quelques **blocs “x-…” bien nommés** (ex. `x-service-base`, `x-logging`, `x-healthcheck-http`).
* **Compatibilité** : c’est du YAML standard, donc **fiable** avec Docker Compose V2.

---

## En pratique : workflow conseillé

1. Définis **2–4 blocs** réutilisables au sommet (`x-logging`, `x-healthcheck`, `x-service-base`).
2. Dans chaque service, **fusionne** avec `<<: *service_base`, puis **surcharge** ce qui change.
3. Pour dev/prod, combine avec `-f` (fichiers overlay) et **valide** avec `docker compose -f base -f prod config`.
