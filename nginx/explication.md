# Cours Complet Nginx : Débutant à Expert

## Table des Matières

1. [Introduction à Nginx](#introduction)
2. [Architecture et Concepts Fondamentaux](#architecture)
3. [Syntaxe et Structure de Configuration](#syntaxe)
4. [Serveur Web de Base](#serveur-web)
5. [Reverse Proxy et Load Balancing](#reverse-proxy)
6. [Sécurité Avancée](#securite)
7. [Optimisation des Performances](#performances)
8. [Bonnes Pratiques et Patterns](#bonnes-pratiques)
9. [Projet Complexe Réel](#projet-complexe)
10. [Monitoring et Dépannage](#monitoring)

---

## <a name="introduction"></a>1. Introduction à Nginx

### 🎯 **Qu'est-ce que Nginx et pourquoi l'utiliser ?**

**Problématiques résolues par Nginx :**

| Problème | Solution Nginx | Alternative traditionnelle |
|----------|----------------|----------------------------|
| **Concurrence C10K** (10,000 connexions) | Architecture événementielle asynchrone | Apache (1 processus = 1 connexion) |
| **Latence élevée** | Reverse proxy + cache | Serveurs directs sans optimisation |
| **Single Point of Failure** | Load balancing + health checks | Serveur unique |
| **Complexité SSL** | Termination SSL centralisée | Configuration SSL sur chaque serveur |

**Quand choisir Nginx vs Apache :**

```bash
# Choisir Nginx quand :
# - Haut débit et nombreuses connexions simultanées
# - Reverse proxy et load balancing
# - Service de cache HTTP
# - Ressources limitées (mémoire, CPU)

# Choisir Apache quand :
# - Configuration .htaccess dynamique
# - Modules personnalisés complexes
# - Environnement WordPress avec nombreuses réécritures
```

### 📊 **Chiffres clés :**
- **10x** plus efficace qu'Apache en charge mémoire
- **Jusqu'à 50,000** connexions simultanées par worker
- **Réduction de 80%** de la latence avec le caching
- **Support natif** HTTP/2, WebSocket, gRPC

---

## <a name="architecture"></a>2. Architecture et Concepts Fondamentaux

### 🏗️ **Architecture Événementielle Détaillée**

**Modèle Traditionnel (Apache) :**
```bash
# Modèle "one thread per connection"
Processus 1 → Connexion 1
Processus 2 → Connexion 2
...
Processus N → Connexion N
# Problème : Consommation mémoire exponentielle
```

**Modèle Nginx :**
```bash
# Modèle asynchrone non-bloquant
Worker 1 → Connexions 1-10,000 (événements)
Worker 2 → Connexions 10,001-20,000
Worker 3 → Connexions 20,001-30,000
# Avantage : Faible consommation mémoire
```

### 🔧 **Composants Architecturels**

```
Nginx Master Process (PID 1)
    │
    ├── Worker Process 1 (traite 10,000 connexions)
    ├── Worker Process 2 (traite 10,000 connexions)
    ├── Cache Loader (charge le cache au démarrage)
    └── Cache Manager (nettoie le cache périodiquement)
```

**Explication des rôles :**
- **Master Process** : Gère les workers, relève la configuration
- **Worker Processes** : Traitent les requêtes réelles
- **Cache Loader/Manager** : Gèrent le cache HTTP

### ⚙️ **Paramètres Clés de l'Architecture**

```nginx
# /etc/nginx/nginx.conf

# Nombre de workers = nombre de CPUs
worker_processes auto;

# Limite de fichiers ouverts par worker
worker_rlimit_nofile 65535;

events {
    # Connexions simultanées par worker
    worker_connections 1024;
    
    # Optimisation : accepter multiples connexions
    multi_accept on;
    
    # Méthode d'événements (epoll sur Linux)
    use epoll;
}
```

**Quand ajuster ces paramètres :**

| Scénario | worker_processes | worker_connections |
|----------|------------------|-------------------|
| **Serveur dédié 4 CPUs** | `4` ou `auto` | `4096` |
| **VPS 2 CPUs** | `2` | `2048` |
| **Environnement conteneurisé** | `1` | `1024` |

---

## <a name="syntaxe"></a>3. Syntaxe et Structure de Configuration

### 📝 **Syntaxe de Base Nginx**

**Structure hiérarchique :**
```nginx
# Commentaires avec #
directive valeur;

# Blocs de contexte
contexte {
    directive valeur;
    
    sous-contexte {
        directive valeur;
    }
}
```

**Contextes principaux :**
```nginx
# Contexte global (hors de tout bloc)
user nginx;
worker_processes auto;

# Contexte events
events {
    worker_connections 1024;
}

# Contexte http
http {
    # Configuration HTTP globale
    
    # Contexte server
    server {
        # Configuration serveur virtuel
        
        # Contexte location
        location / {
            # Configuration spécifique à l'URI
        }
    }
}
```

### 🎯 **Directives Importantes par Contexte**

**Contexte HTTP (global) :**
```nginx
http {
    # Optimisation des performances
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    
    # Timeouts
    keepalive_timeout 65;
    client_body_timeout 12;
    client_header_timeout 12;
    send_timeout 10;
    
    # Buffer sizes
    client_body_buffer_size 16K;
    client_header_buffer_size 1k;
    client_max_body_size 8m;
    large_client_header_buffers 2 1k;
    
    # Compression
    gzip on;
    gzip_types text/plain text/css application/json;
}
```

**Contexte Server (hôte virtuel) :**
```nginx
server {
    # Écoute sur le port 80 pour tous les noms
    listen 80;
    
    # Écoute sur le port 443 avec SSL
    listen 443 ssl http2;
    
    # Nom du serveur (virtual host)
    server_name example.com www.example.com;
    
    # Racine des documents
    root /var/www/html;
    
    # Fichier d'index par défaut
    index index.html index.htm;
}
```

**Contexte Location (routage) :**
```nginx
location [modificateur] uri {
    # Configuration spécifique à l'URI
}
```

**Modificateurs de location :**

| Modificateur | Signification | Priorité |
|-------------|---------------|----------|
| `= /exact` | Correspondance exacte | 1 (plus haute) |
| `^~ /prefix` | Préfixe prioritaire | 2 |
| `~ regex` | Regex sensible à la casse | 3 |
| `~* regex` | Regex insensible à la casse | 3 |
| `/prefix` | Préfixe simple | 4 |
| `/` | Location par défaut | 5 (plus basse) |

**Exemple d'ordre d'évaluation :**
```nginx
location = /admin {        # 1. Exact match - priorité haute
    return 403;
}

location ^~ /static/ {     # 2. Priority prefix
    try_files $uri =404;
}

location ~* \.(js|css)$ {  # 3. Regex case insensitive
    expires 1y;
}

location / {               # 4. Prefix match - priorité basse
    try_files $uri $uri/ /index.html;
}
```

---

## <a name="serveur-web"></a>4. Serveur Web de Base

### 🚀 **Configuration d'un Site Web Simple**

**Structure de fichiers recommandée :**
```
/var/www/
├── mon-site/
│   ├── index.html
│   ├── css/
│   ├── js/
│   └── images/
/etc/nginx/
├── nginx.conf
├── sites-available/
│   └── mon-site
└── sites-enabled/
    └── mon-site -> ../sites-available/mon-site
```

**Configuration complète :**
```nginx
# /etc/nginx/sites-available/mon-site

server {
    # Écoute sur le port 80 pour IPv4 et IPv6
    listen 80;
    listen [::]:80;
    
    # Noms de domaine pour ce serveur virtuel
    server_name mon-site.com www.mon-site.com;
    
    # Racine des documents - CHEMIN ABSOLU requis
    root /var/www/mon-site;
    
    # Fichiers d'index dans l'ordre de priorité
    index index.html index.htm index.php;
    
    # Logs spécifiques au site
    access_log /var/log/nginx/mon-site-access.log;
    error_log /var/log/nginx/mon-site-error.log;
    
    # Configuration par défaut pour toutes les locations
    location / {
        # Essaye de servir le fichier, puis le dossier, puis 404
        try_files $uri $uri/ =404;
        
        # Sécurité : pas de listing de répertoire
        autoindex off;
    }
    
    # Gestion des fichiers statiques avec cache long
    location ~* \.(jpg|jpeg|png|gif|ico|css|js|pdf|txt)$ {
        # Cache pour 1 an
        expires 1y;
        
        # Headers de cache
        add_header Cache-Control "public, immutable";
        
        # Pas de log pour les assets statiques (performance)
        access_log off;
        
        # Essaye de servir le fichier ou 404
        try_files $uri =404;
    }
    
    # Protection des fichiers sensibles
    location ~ /\. {
        deny all;
        access_log off;
        log_not_found off;
    }
    
    location ~ /(config|database|env) {
        deny all;
    }
    
    # Page d'erreur personnalisée
    error_page 404 /404.html;
    error_page 500 502 503 504 /50x.html;
    
    location = /50x.html {
        root /usr/share/nginx/html;
    }
}
```

### 🔧 **Activation du Site**

```bash
# Créer le lien symbolique (méthode Debian/Ubuntu)
sudo ln -s /etc/nginx/sites-available/mon-site /etc/nginx/sites-enabled/

# Test de la configuration
sudo nginx -t

# Rechargement de Nginx
sudo systemctl reload nginx

# Vérification du statut
sudo systemctl status nginx
```

### 🎯 **Quand utiliser cette configuration :**

- **Site vitrine statique** : Portfolio, blog statique
- **Application SPA** : React, Vue, Angular
- **Landing page** : Page de présentation simple
- **Site de démonstration** : Preuve de concept

---

## <a name="reverse-proxy"></a>5. Reverse Proxy et Load Balancing

### 🔄 **Reverse Proxy - Concepts**

**Problème résolu :**
```
Client → Nginx (reverse proxy) → Application Backend (Node.js, Python, Java)
```

**Avantages :**
- **Terminaison SSL** : Gestion centralisée des certificats
- **Cache** : Réduction de la charge backend
- **Sécurité** : Masquage de l'infrastructure backend
- **Load Balancing** : Répartition de charge

### ⚙️ **Configuration Reverse Proxy de Base**

```nginx
server {
    listen 80;
    server_name api.mon-site.com;
    
    location / {
        # Proxy vers l'application backend
        proxy_pass http://localhost:3000;
        
        # Headers importants pour le backend
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts
        proxy_connect_timeout 5s;
        proxy_send_timeout 10s;
        proxy_read_timeout 30s;
        
        # Buffer optimisation
        proxy_buffering on;
        proxy_buffer_size 4k;
        proxy_buffers 8 4k;
    }
}
```

### ⚖️ **Load Balancing - Configuration Avancée**

**Définition des backends :**
```nginx
upstream backend_servers {
    # Algorithmes disponibles :
    # round-robin (défaut), least_conn, ip_hash, hash
    
    least_conn;  # Préfère le serveur avec le moins de connexions
    
    server 192.168.1.10:8080 weight=3;  # 3x plus de trafic
    server 192.168.1.11:8080 weight=2;
    server 192.168.1.12:8080;           # weight=1 par défaut
    server 192.168.1.13:8080 backup;    # Serveur de secours
    server 192.168.1.14:8080 down;      # Serveur désactivé
}
```

**Configuration du load balancer :**
```nginx
server {
    listen 80;
    server_name app.mon-site.com;
    
    location / {
        proxy_pass http://backend_servers;
        
        # Gestion des erreurs de backend
        proxy_next_upstream error timeout invalid_header http_500 http_502 http_503 http_504;
        proxy_next_upstream_tries 3;
        proxy_next_upstream_timeout 10s;
        
        # Health check implicite
        proxy_connect_timeout 2s;
        proxy_read_timeout 10s;
        
        # Headers
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # Endpoint de health check
    location /health {
        access_log off;
        proxy_pass http://backend_servers/health;
    }
}
```

### 🎯 **Quand utiliser Reverse Proxy vs Load Balancing :**

| Scénario | Solution | Configuration |
|----------|----------|---------------|
| **Application monolithique** | Reverse Proxy simple | `proxy_pass http://localhost:3000` |
| **Microservices multiples** | Reverse Proxy + routing | Locations avec différents `proxy_pass` |
| **Haute disponibilité** | Load Balancing | `upstream` avec multiples serveurs |
| **Session persistante** | Load Balancing + `ip_hash` | `ip_hash` dans `upstream` |
| **Canary deployment** | Load Balancing + poids | `server backend weight=1` |

### 🔧 **Exemple Microservices :**

```nginx
upstream users_service {
    server 10.0.1.10:3001;
    server 10.0.1.11:3001;
}

upstream products_service {
    server 10.0.1.20:3002;
    server 10.0.1.21:3002;
}

upstream orders_service {
    server 10.0.1.30:3003;
}

server {
    listen 80;
    server_name api.company.com;
    
    location /api/users/ {
        proxy_pass http://users_service/;
        proxy_set_header X-Service users;
    }
    
    location /api/products/ {
        proxy_pass http://products_service/;
        proxy_set_header X-Service products;
    }
    
    location /api/orders/ {
        proxy_pass http://orders_service/;
        proxy_set_header X-Service orders;
    }
}
```

---

## <a name="securite"></a>6. Sécurité Avancée

### 🛡️ **Hardening de Nginx**

**Configuration de sécurité de base :**
```nginx
http {
    # Masquer la version de Nginx
    server_tokens off;
    
    # Headers de sécurité
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' https: data: 'unsafe-inline' 'unsafe-eval'" always;
    
    # Protection contre les attaques
    client_body_buffer_size 16k;
    client_header_buffer_size 1k;
    client_max_body_size 10m;
    large_client_header_buffers 4 8k;
}
```

**Rate Limiting :**
```nginx
# Zones de limitation
limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
limit_req_zone $binary_remote_addr zone=auth:10m rate=2r/m;
limit_req_zone $binary_remote_addr zone=search:10m rate=5r/s;

server {
    location /api/ {
        limit_req zone=api burst=20 nodelay;
        proxy_pass http://backend;
    }
    
    location /auth/login {
        limit_req zone=auth burst=5 nodelay;
        proxy_pass http://backend;
    }
    
    location /search {
        limit_req zone=search burst=10 nodelay;
        proxy_pass http://backend;
    }
    
    # Gestion des erreurs de rate limiting
    error_page 429 /429.html;
    location = /429.html {
        root /usr/share/nginx/html;
        internal;
    }
}
```

### 🔐 **SSL/TLS Avancé**

```nginx
server {
    listen 443 ssl http2;
    server_name mon-site.com;
    
    # Certificats
    ssl_certificate /etc/ssl/certs/mon-site.com.crt;
    ssl_certificate_key /etc/ssl/private/mon-site.com.key;
    
    # Configuration SSL sécurisée
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;
    ssl_prefer_server_ciphers off;
    
    # Performance SSL
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    ssl_session_tickets off;
    
    # OCSP Stapling
    ssl_stapling on;
    ssl_stapling_verify on;
    
    # HSTS (Force HTTPS)
    add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;
    
    # DH Parameters (générer avec: openssl dhparam -out /etc/ssl/dhparam.pem 2048)
    ssl_dhparam /etc/ssl/dhparam.pem;
}
```

### 🚫 **Protection contre les attaques courantes**

```nginx
# Protection DDoS - Rate limiting global
limit_req_zone $binary_remote_addr zone=global:10m rate=100r/s;

# Protection contre les bots
location / {
    limit_req zone=global burst=200 nodelay;
    
    # Blocage des user agents malveillants
    if ($http_user_agent ~* (wget|curl|scan|bot|crawl)) {
        return 403;
    }
}

# Protection des endpoints sensibles
location /admin {
    # Restriction IP
    allow 192.168.1.0/24;
    allow 10.0.0.1;
    deny all;
    
    # Authentification basique
    auth_basic "Administration";
    auth_basic_user_file /etc/nginx/.htpasswd;
}

# Protection contre l'inclusion de fichiers
location ~ \.php$ {
    # Désactiver l'exécution de PHP dans les uploads
    location ~ /uploads/.*\.php$ {
        deny all;
    }
}
```

---

## <a name="performances"></a>7. Optimisation des Performances

### 🚀 **Optimisation du Cache**

**Cache HTTP :**
```nginx
http {
    # Configuration du cache
    proxy_cache_path /var/cache/nginx levels=1:2 
                     keys_zone=my_cache:10m 
                     max_size=10g 
                     inactive=60m 
                     use_temp_path=off;
    
    # Paramètres de cache globaux
    proxy_cache_key "$scheme$request_method$host$request_uri";
    proxy_cache_valid 200 302 10m;
    proxy_cache_valid 404 1m;
    
    server {
        location / {
            proxy_cache my_cache;
            proxy_pass http://backend;
            
            # Comportement du cache
            proxy_cache_use_stale error timeout updating 
                                 http_500 http_502 http_503 http_504;
            proxy_cache_background_update on;
            proxy_cache_lock on;
            proxy_cache_lock_timeout 5s;
            
            # Header de débogage
            add_header X-Cache-Status $upstream_cache_status;
        }
        
        # Invalidation du cache
        location ~ /purge(/.*) {
            proxy_cache_purge my_cache "$scheme$request_method$host$1";
        }
    }
}
```

### 📊 **Optimisation des Assets Statiques**

```nginx
server {
    # Compression Gzip
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_comp_level 6;
    gzip_types
        text/plain
        text/css
        text/xml
        text/javascript
        application/json
        application/javascript
        application/xml+rss
        application/atom+xml
        image/svg+xml;
    
    # Cache des fichiers statiques
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
        add_header Vary Accept-Encoding;
        access_log off;
        
        # Optimisation de la livraison
        sendfile on;
        tcp_nopush on;
    }
    
    # Brotli compression (si compilé avec brotli)
    # brotli on;
    # brotli_types text/plain text/css application/json;
}
```

### ⚡ **Optimisation des Connexions**

```nginx
http {
    # Optimisation TCP
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    
    # Keepalive
    keepalive_timeout 30;
    keepalive_requests 100;
    
    # Buffer optimisation
    client_body_buffer_size 16k;
    client_header_buffer_size 1k;
    client_max_body_size 8m;
    large_client_header_buffers 4 8k;
    
    # File descriptor limits
    worker_rlimit_nofile 65535;
    
    events {
        worker_connections 4096;
        multi_accept on;
        use epoll;
    }
}
```

---

## <a name="bonnes-pratiques"></a>8. Bonnes Pratiques et Patterns

### ✅ **Structure de Configuration Recommandée**

```
/etc/nginx/
├── nginx.conf                  # Configuration principale
├── conf.d/
│   ├── security.conf           # Headers de sécurité
│   ├── compression.conf        # Configuration compression
│   ├── caching.conf           # Configuration cache
│   └── rate-limiting.conf     # Rate limiting
├── sites-available/
│   ├── frontend.conf
│   ├── api.conf
│   └── admin.conf
├── sites-enabled/              # Liens symboliques
├── ssl/                        # Certificats SSL
├── includes/                   # Fichiers inclus
│   ├── proxy-settings.conf
│   └── security-headers.conf
└── snippets/                   # Fragments réutilisables
    ├── ssl-params.conf
    └── security.conf
```

### 🔧 **Fichier nginx.conf Principal**

```nginx
# /etc/nginx/nginx.conf

user www-data;
worker_processes auto;
pid /run/nginx.pid;

# Chargement des modules
include /etc/nginx/modules-enabled/*.conf;

events {
    worker_connections 4096;
    multi_accept on;
    use epoll;
}

http {
    # Inclusions de base
    include /etc/nginx/mime.types;
    include /etc/nginx/conf.d/*.conf;
    include /etc/nginx/sites-enabled/*;
    
    # Paramètres par défaut
    default_type application/octet-stream;
    
    # Logging
    access_log /var/log/nginx/access.log;
    error_log /var/log/nginx/error.log;
}
```

### 🎯 **Quand utiliser chaque fonctionnalité :**

| Scénario | Fonctionnalité | Configuration |
|----------|---------------|---------------|
| **Site statique simple** | Serveur web basique | `try_files $uri $uri/ =404` |
| **Application dynamique** | Reverse proxy | `proxy_pass` + headers |
| **API REST** | Load balancing + cache | `upstream` + `proxy_cache` |
| **E-commerce** | SSL + sécurité + cache | SSL hardening + WAF |
| **Media streaming** | Optimisation fichiers | `sendfile` + cache |
| **Microservices** | API Gateway | Multiple `location` + `upstream` |

### ⚠️ **Erreurs Courantes à Éviter :**

```nginx
# MAUVAIS - if dans location est dangereux
location / {
    if ($uri ~* \.php$) {
        proxy_pass http://php_backend;
    }
}

# BON - Utiliser des locations séparées
location ~ \.php$ {
    proxy_pass http://php_backend;
}

# MAUVAIS - Redirection dans le bloc server
server {
    listen 80;
    return 301 https://$host$request_uri;
}

# BON - Serveur dédié pour la redirection
server {
    listen 80;
    server_name _;
    return 301 https://$host$request_uri;
}
```

---

## <a name="projet-complexe"></a>9. Projet Complexe Réel

### 🏗️ **Architecture E-commerce avec Microservices**

```
Clients → Nginx (API Gateway + Load Balancer)
                │
                ├── Service Frontend (React)
                ├── Service Utilisateurs (Node.js)
                ├── Service Produits (Python)
                ├── Service Commandes (Java)
                ├── Service Paiements (Go)
                └── Service Notifications (Node.js)
```

### 🔧 **Configuration Complète**

**Fichier de configuration principal :**
```nginx
# /etc/nginx/nginx.conf

user www-data;
worker_processes auto;
pid /run/nginx.pid;

events {
    worker_connections 4096;
    multi_accept on;
    use epoll;
}

http {
    # Paramètres de base
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 30;
    types_hash_max_size 2048;
    server_tokens off;
    
    # MIME Types
    include /etc/nginx/mime.types;
    default_type application/octet-stream;
    
    # Logging format étendu
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for" '
                    'rt=$request_time uct="$upstream_connect_time" '
                    'uht="$upstream_header_time" urt="$upstream_response_time"';
    
    access_log /var/log/nginx/access.log main;
    error_log /var/log/nginx/error.log warn;
    
    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=100r/s;
    limit_req_zone $binary_remote_addr zone=auth:10m rate=5r/m;
    limit_req_zone $binary_remote_addr zone=checkout:10m rate=10r/m;
    
    # Cache
    proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=api_cache:10m
                     max_size=10g inactive=60m use_temp_path=off;
    
    # Upstreams
    upstream frontend {
        server 10.0.1.10:3000;
        server 10.0.1.11:3000;
    }
    
    upstream users_service {
        least_conn;
        server 10.0.1.20:3001;
        server 10.0.1.21:3001;
    }
    
    upstream products_service {
        least_conn;
        server 10.0.1.30:3002;
        server 10.0.1.31:3002;
    }
    
    upstream orders_service {
        server 10.0.1.40:3003;
    }
    
    upstream payments_service {
        server 10.0.1.50:3004;
    }
    
    # Inclusions
    include /etc/nginx/conf.d/*.conf;
    include /etc/nginx/sites-enabled/*;
}
```

**Gateway API :**
```nginx
# /etc/nginx/sites-available/api-gateway

# API Gateway
server {
    listen 443 ssl http2;
    server_name api.mon-ecommerce.com;
    
    # SSL
    ssl_certificate /etc/ssl/certs/mon-ecommerce.com.crt;
    ssl_certificate_key /etc/ssl/private/mon-ecommerce.com.key;
    include /etc/nginx/snippets/ssl-params.conf;
    
    # Headers de sécurité
    include /etc/nginx/snippets/security-headers.conf;
    
    # Logs
    access_log /var/log/nginx/api-gateway-access.log main;
    error_log /var/log/nginx/api-gateway-error.log;
    
    # Service Utilisateurs
    location /api/users/ {
        limit_req zone=api burst=50 nodelay;
        
        # Validation JWT
        auth_request /_validate_token;
        
        proxy_pass http://users_service/;
        include /etc/nginx/includes/proxy-settings.conf;
        
        # Headers spécifiques
        proxy_set_header X-User-ID $jwt_sub;
        proxy_set_header X-User-Roles $jwt_roles;
    }
    
    # Service Produits (avec cache)
    location /api/products/ {
        limit_req zone=api burst=100 nodelay;
        
        proxy_pass http://products_service/;
        include /etc/nginx/includes/proxy-settings.conf;
        
        # Cache des produits
        proxy_cache api_cache;
        proxy_cache_valid 200 302 10m;
        proxy_cache_valid 404 1m;
        proxy_cache_methods GET HEAD;
        proxy_cache_key "$scheme$request_method$host$request_uri";
        
        add_header X-Cache-Status $upstream_cache_status;
    }
    
    # Service Commandes
    location /api/orders/ {
        limit_req zone=api burst=30 nodelay;
        
        auth_request /_validate_token;
        
        proxy_pass http://orders_service/;
        include /etc/nginx/includes/proxy-settings.conf;
        proxy_set_header X-User-ID $jwt_sub;
    }
    
    # Service Paiements (rate limiting strict)
    location /api/payments/ {
        limit_req zone=checkout burst=5 nodelay;
        
        auth_request /_validate_token;
        
        # Pas de cache pour les paiements
        proxy_buffering off;
        
        proxy_pass http://payments_service/;
        include /etc/nginx/includes/proxy-settings.conf;
        proxy_set_header X-User-ID $jwt_sub;
        
        # Timeouts plus longs
        proxy_connect_timeout 10s;
        proxy_send_timeout 30s;
        proxy_read_timeout 60s;
    }
    
    # Endpoint de validation de token (interne)
    location = /_validate_token {
        internal;
        
        proxy_pass http://users_service/auth/validate;
        proxy_pass_request_body off;
        proxy_set_header Content-Length "";
        proxy_set_header X-Original-URI $request_uri;
    }
    
    # Login (rate limiting strict)
    location /api/auth/login {
        limit_req zone=auth burst=3 nodelay;
        
        proxy_pass http://users_service/auth/login;
        include /etc/nginx/includes/proxy-settings.conf;
    }
    
    # Health checks
    location /health {
        access_log off;
        
        # Check de tous les services
        proxy_pass http://users_service/health;
        include /etc/nginx/includes/proxy-settings.conf;
    }
    
    # Gestion des erreurs
    error_page 500 502 503 504 /50x.json;
    location = /50x.json {
        return 503 '{"error":"Service temporarily unavailable"}';
        add_header Content-Type application/json;
    }
    
    error_page 429 /429.json;
    location = /429.json {
        return 429 '{"error":"Too many requests"}';
        add_header Content-Type application/json;
    }
}
```

**Frontend :**
```nginx
# /etc/nginx/sites-available/frontend

server {
    listen 443 ssl http2;
    server_name mon-ecommerce.com www.mon-ecommerce.com;
    
    root /var/www/frontend/dist;
    index index.html;
    
    # SSL
    ssl_certificate /etc/ssl/certs/mon-ecommerce.com.crt;
    ssl_certificate_key /etc/ssl/private/mon-ecommerce.com.key;
    include /etc/nginx/snippets/ssl-params.conf;
    
    # Headers de sécurité
    include /etc/nginx/snippets/security-headers.conf;
    
    # Cache des assets statiques
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
        access_log off;
    }
    
    # Configuration SPA
    location / {
        try_files $uri $uri/ /index.html;
        add_header Cache-Control "no-cache, no-store, must-revalidate";
    }
    
    # Proxy vers l'API
    location /api/ {
        proxy_pass https://api.mon-ecommerce.com;
        include /etc/nginx/includes/proxy-settings.conf;
    }
    
    # Service Worker
    location /sw.js {
        add_header Cache-Control "no-cache, no-store, must-revalidate";
        add_header Content-Type "application/javascript";
    }
}

# Redirection HTTP → HTTPS
server {
    listen 80;
    server_name mon-ecommerce.com www.mon-ecommerce.com;
    return 301 https://$server_name$request_uri;
}
```

**Fichiers inclus :**
```nginx
# /etc/nginx/includes/proxy-settings.conf

proxy_http_version 1.1;
proxy_set_header Upgrade $http_upgrade;
proxy_set_header Connection 'upgrade';
proxy_set_header Host $host;
proxy_set_header X-Real-IP $remote_addr;
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
proxy_set_header X-Forwarded-Proto $scheme;
proxy_cache_bypass $http_upgrade;

# Timeouts
proxy_connect_timeout 5s;
proxy_send_timeout 10s;
proxy_read_timeout 30s;

# Buffer optimisation
proxy_buffering on;
proxy_buffer_size 4k;
proxy_buffers 8 4k;
```

---

## <a name="monitoring"></a>10. Monitoring et Dépannage

### 🔍 **Commandes Essentielles de Dépannage**

```bash
# Test de configuration
sudo nginx -t

# Test avec affichage complet
sudo nginx -T

# Rechargement sécurisé
sudo nginx -s reload

# Arrêt gracieux
sudo nginx -s quit

# Rechargement des certificats SSL
sudo nginx -s reload

# Vérification des ports ouverts
sudo netstat -tulpn | grep nginx

# Surveillance des logs en temps réel
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# Test de performance
ab -n 1000 -c 10 https://mon-site.com/
```

### 📊 **Monitoring avec Stub Status**

```nginx
# Configuration du module stub_status
server {
    listen 8080;
    server_name 127.0.0.1;
    
    location /nginx-status {
        stub_status on;
        access_log off;
        allow 127.0.0.1;
        deny all;
    }
    
    location /server-status {
        # Status étendu
        stub_status on;
        access_log off;
        allow 127.0.0.1;
        deny all;
    }
}
```

### 🛠️ **Script de Diagnostic Complet**

```bash
#!/bin/bash
# nginx-diagnostic.sh

echo "🔍 Diagnostic complet Nginx"

# Fonctions de vérification
check_nginx_running() {
    if systemctl is-active --quiet nginx; then
        echo "✅ Nginx est en cours d'exécution"
        return 0
    else
        echo "❌ Nginx n'est pas en cours d'exécution"
        return 1
    fi
}

check_nginx_config() {
    echo "🧪 Test de configuration..."
    if nginx -t; then
        echo "✅ Configuration valide"
        return 0
    else
        echo "❌ Erreur de configuration"
        return 1
    fi
}

check_ports() {
    echo "🔌 Vérification des ports..."
    local ports=("80" "443")
    for port in "${ports[@]}"; do
        if ss -tuln | grep ":$port " > /dev/null; then
            echo "✅ Port $port en écoute"
        else
            echo "❌ Port $port non accessible"
        fi
    done
}

check_ssl_certificates() {
    echo "📜 Vérification des certificats SSL..."
    local domains=("mon-ecommerce.com" "api.mon-ecommerce.com")
    for domain in "${domains[@]}"; do
        if openssl s_client -connect $domain:443 -servername $domain < /dev/null 2>/dev/null | openssl x509 -noout -dates > /dev/null 2>&1; then
            echo "✅ Certificat SSL valide pour $domain"
            # Vérification de l'expiration
            openssl s_client -connect $domain:443 -servername $domain < /dev/null 2>/dev/null | openssl x509 -noout -dates | grep notAfter
        else
            echo "❌ Problème avec le certificat SSL pour $domain"
        fi
    done
}

check_performance() {
    echo "📊 Analyse de performance..."
    
    # Connexions actives
    local connections=$(ss -t state established sport = :80 or sport = :443 | wc -l)
    echo "📈 Connexions actives: $((connections-1))"
    
    # Mémoire utilisée
    local memory=$(ps -o rss= -C nginx | awk '{sum+=$1} END {print sum/1024 " MB"}')
    echo "💾 Mémoire utilisée: $memory"
    
    # Requêtes par seconde (approximatif)
    local rps=$(tail -1000 /var/log/nginx/access.log 2>/dev/null | wc -l)
    echo "⚡ Requêtes (derniers 1000 logs): $rps"
}

check_error_logs() {
    echo "📋 Analyse des erreurs récentes..."
    if [[ -f "/var/log/nginx/error.log" ]]; then
        local recent_errors=$(tail -20 /var/log/nginx/error.log | grep -i error | wc -l)
        echo "🚨 Erreurs récentes (20 lignes): $recent_errors"
        
        if [[ $recent_errors -gt 0 ]]; then
            echo "🔍 Dernières erreurs:"
            tail -5 /var/log/nginx/error.log | grep -i error
        fi
    else
        echo "⚠️ Fichier error.log non trouvé"
    fi
}

# Exécution des vérifications
main() {
    echo "========================================="
    echo "       DIAGNOSTIC NGINX COMPLET"
    echo "========================================="
    
    check_nginx_running
    check_nginx_config
    check_ports
    check_ssl_certificates
    check_performance
    check_error_logs
    
    echo "========================================="
    echo "✅ Diagnostic terminé"
}

main
```

### 📈 **Analyse des Logs avec Outils Avancés**

```bash
# Top 10 des IPs les plus actives
awk '{print $1}' /var/log/nginx/access.log | sort | uniq -c | sort -nr | head -10

# Requêtes les plus fréquentes
awk '{print $7}' /var/log/nginx/access.log | sort | uniq -c | sort -nr | head -10

# Codes de statut HTTP
awk '{print $9}' /var/log/nginx/access.log | sort | uniq -c | sort -nr

# Temps de réponse par endpoint
awk '{print $7, $NF}' /var/log/nginx/access.log | sort | head -20

# Erreurs 5xx
grep '" 5[0-9][0-9] ' /var/log/nginx/access.log | awk '{print $7, $9}' | sort | uniq -c | sort -nr

# Bandwidth par endpoint
awk '{print $7, $10}' /var/log/nginx/access.log | awk '{array[$1]+=$2} END {for (i in array) print i, array[i]}' | sort -nr -k2 | head -10
```

## 🎓 **Conclusion**

Ce cours complet vous a permis de passer de **débutant à expert** en couvrant :

### ✅ **Niveau Débutant :**
- Compréhension de l'architecture Nginx
- Configuration basique d'un serveur web
- Gestion des sites simples

### ✅ **Niveau Intermédiaire :**
- Reverse proxy et load balancing
- Configuration SSL/TLS
- Optimisation des performances

### ✅ **Niveau Expert :**
- Architecture microservices complexe
- Sécurité avancée et hardening
- Monitoring et diagnostic professionnel

### 🚀 **Prochaines Étapes :**
1. **Automatisation** avec Ansible/Terraform
2. **Containerisation** avec Docker/Kubernetes
3. **CI/CD** pour le déploiement Nginx
4. **WAF** (Web Application Firewall) avancé
5. **Service Mesh** avec Nginx comme sidecar

Nginx reste un outil essentiel et polyvalent qui, maîtrisé, peut résoudre la majorité des défis d'infrastructure web moderne.