# Cours Complet : Génération de SSL avec Let's Encrypt, Certbot et Nginx

## Table des Matières
1. [Introduction au SSL/TLS](#introduction)
2. [Let's Encrypt et Certbot](#lets-encrypt)
3. [Installation et Configuration](#installation)
4. [Domaines et Sous-domaines](#domaines)
5. [Configurations Nginx Avancées](#nginx-avancé)
6. [Bonnes Pratiques Professionnelles](#bonnes-pratiques)
7. [Automatisation et Renouvellement](#automatisation)
8. [Dépannage Avancé](#depannage)

---

## 1. Introduction au SSL/TLS <a name="introduction"></a>

### Qu'est-ce que SSL/TLS ?
- **SSL (Secure Sockets Layer)** : Protocole de sécurisation des échanges sur Internet
- **TLS (Transport Layer Security)** : Successeur de SSL, version moderne et sécurisée
- **Fonction** : Chiffrement des données, authentification, intégrité

### Pourquoi utiliser SSL ?
- **Sécurité** : Protection des données sensibles
- **Confiance** : Indicateur visuel (cadenas) pour les utilisateurs
- **SEO** : Facteur de ranking Google
- **Performance** : HTTP/2 nécessite SSL

### Types de certificats
- **DV (Domain Validation)** : Validation basique du domaine
- **OV (Organization Validation)** : Validation de l'organisation
- **EV (Extended Validation)** : Validation étendue (barre verte)

---

## 2. Let's Encrypt et Certbot <a name="lets-encrypt"></a>

### Let's Encrypt
- **Autorité de certification** gratuite et automatisée
- **Certificats DV** uniquement
- **Validité** : 90 jours (renouvellement obligatoire)
- **ACME Protocol** : Automatisation des processus

### Certbot
- **Client officiel** Let's Encrypt
- **Automatisation** complète du processus
- **Plugins** pour différents serveurs web

---

## 3. Installation et Configuration <a name="installation"></a>

### Installation de base

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install certbot python3-certbot-nginx

# CentOS/RHEL
sudo yum install certbot python3-certbot-nginx

# Installation via Snap (recommandé)
sudo snap install --classic certbot
sudo ln -s /snap/bin/certbot /usr/bin/certbot
```

### Première configuration

```bash
# Certificat simple pour un domaine
sudo certbot --nginx -d example.com -d www.example.com

# Mode manuel (sans modification automatique de Nginx)
sudo certbot certonly --nginx -d example.com
```

### Structure des fichiers générés
```
/etc/letsencrypt/
├── live/
│   └── example.com/
│       ├── cert.pem          # Certificat public
│       ├── privkey.pem       # Clé privée
│       ├── chain.pem         # Chaîne de certificats
│       └── fullchain.pem     # Certificat + chaîne
├── archive/
└── renewal/
```

---

## 4. Domaines et Sous-domaines <a name="domaines"></a>

### Certificat unique pour domaine + sous-domaines

```bash
# Certificat couvrant domaine et sous-domaines
sudo certbot --nginx -d example.com -d www.example.com -d api.example.com -d shop.example.com
```

### Certificat wildcard (générique)

```bash
# Pour tous les sous-domaines
sudo certbot --nginx -d "*.example.com" -d example.com

# Authentification DNS (nécessaire pour wildcard)
sudo certbot certonly --manual --preferred-challenges dns -d "*.example.com" -d example.com
```

### Configuration Nginx pour multiples domaines

```nginx
# Serveur principal
server {
    listen 443 ssl http2;
    server_name example.com www.example.com;
    
    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;
    
    # Configuration SSL commune
    include /etc/nginx/snippets/ssl-params.conf;
    
    location / {
        # Configuration de l'application
    }
}

# Sous-domaine API
server {
    listen 443 ssl http2;
    server_name api.example.com;
    
    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;
    
    include /etc/nginx/snippets/ssl-params.conf;
    
    location / {
        # Configuration API
    }
}
```

---

## 5. Configurations Nginx Avancées <a name="nginx-avancé"></a>

### Configuration SSL Optimisée

```nginx
# /etc/nginx/snippets/ssl-params.conf
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
ssl_prefer_server_ciphers off;
ssl_session_cache shared:SSL:10m;
ssl_session_timeout 1d;
ssl_session_tickets off;

# OCSP Stapling
ssl_stapling on;
ssl_stapling_verify on;
resolver 8.8.8.8 8.8.4.4 valid=300s;
resolver_timeout 5s;

# Headers de sécurité
add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;
add_header X-Frame-Options DENY;
add_header X-Content-Type-Options nosniff;
```

### Redirection HTTP vers HTTPS

```nginx
# Redirection forcée HTTP → HTTPS
server {
    listen 80;
    server_name example.com www.example.com api.example.com;
    return 301 https://$host$request_uri;
}

# Serveur HTTPS principal
server {
    listen 443 ssl http2;
    server_name example.com www.example.com;
    
    # Configuration SSL
    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;
    
    include /etc/nginx/snippets/ssl-params.conf;
    
    # Votre configuration d'application
    root /var/www/html;
    index index.html;
}
```

### Configuration pour Load Balancer

```nginx
# Serveur frontal avec SSL termination
server {
    listen 443 ssl http2;
    server_name example.com;
    
    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;
    
    include /etc/nginx/snippets/ssl-params.conf;
    
    location / {
        proxy_pass http://backend_pool;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

upstream backend_pool {
    server 10.0.1.10:80;
    server 10.0.1.11:80;
    server 10.0.1.12:80;
}
```

---

## 6. Bonnes Pratiques Professionnelles <a name="bonnes-pratiques"></a>

### Sécurité

```nginx
# Configuration de sécurité renforcée
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers 'TLS13-CHACHA20-POLY1305-SHA256:TLS13-AES-256-GCM-SHA384:TLS13-AES-128-GCM-SHA256:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384';
ssl_prefer_server_ciphers off;

# Désactivation des anciennes versions SSL
ssl_protocols TLSv1.2 TLSv1.3;
```

### Performance

```nginx
# Optimisations performances SSL
ssl_session_cache shared:SSL:50m;
ssl_session_timeout 1d;
ssl_buffer_size 4k;

# Réutilisation de session pour les clients mobiles
ssl_session_tickets on;
```

### Monitoring et Logs

```nginx
# Logs SSL détaillés
log_format ssl_log '$remote_addr - $remote_user [$time_local] '
                   '"$request" $status $body_bytes_sent '
                   '"$http_referer" "$http_user_agent" '
                   'ssl_protocol:$ssl_protocol '
                   'ssl_cipher:$ssl_cipher';

access_log /var/log/nginx/ssl_access.log ssl_log;
```

### Script de déploiement sécurisé

```bash
#!/bin/bash
# deploy-ssl.sh

DOMAIN="example.com"
EMAIL="admin@example.com"

# Arrêt temporaire de Nginx pour Certbot standalone
sudo systemctl stop nginx

# Obtention du certificat
sudo certbot certonly --standalone --preferred-challenges http \
    -d $DOMAIN \
    -d www.$DOMAIN \
    -d api.$DOMAIN \
    --email $EMAIL \
    --agree-tos \
    --non-interactive

# Redémarrage de Nginx
sudo systemctl start nginx

# Test de la configuration
sudo nginx -t && sudo systemctl reload nginx

# Vérification SSL
echo "Vérification du certificat:"
openssl s_client -connect $DOMAIN:443 -servername $DOMAIN < /dev/null 2>/dev/null | openssl x509 -noout -dates
```

---

## 7. Automatisation et Renouvellement <a name="automatisation"></a>

### Renouvellement automatique

```bash
# Test de renouvellement (dry run)
sudo certbot renew --dry-run

# Renouvellement manuel
sudo certbot renew

# Création d'un cron job automatique
echo "0 12 * * * /usr/bin/certbot renew --quiet" | sudo tee -a /etc/crontab > /dev/null
```

### Script d'automatisation avancé

```bash
#!/bin/bash
# ssl-auto-renew.sh

LOG_FILE="/var/log/ssl-renewal.log"
DOMAINS=("example.com" "www.example.com" "api.example.com")

echo "$(date): Début du renouvellement SSL" >> $LOG_FILE

# Renouvellement
if certbot renew --quiet; then
    echo "$(date): Renouvellement réussi" >> $LOG_FILE
    
    # Rechargement de Nginx
    systemctl reload nginx
    echo "$(date): Nginx rechargé" >> $LOG_FILE
    
    # Notification (exemple avec curl pour Slack/Webhook)
    curl -X POST -H 'Content-type: application/json' \
    --data '{"text":"SSL certificates renewed successfully for '"${DOMAINS[*]}"'"}' \
    https://hooks.slack.com/services/YOUR/WEBHOOK/URL >> $LOG_FILE 2>&1
else
    echo "$(date): Échec du renouvellement" >> $LOG_FILE
    exit 1
fi
```

### Configuration avec Docker

```yaml
# docker-compose.yml
version: '3.8'

services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - /etc/letsencrypt:/etc/letsencrypt:ro
      - ./html:/usr/share/nginx/html
    depends_on:
      - certbot
  
  certbot:
    image: certbot/certbot
    volumes:
      - /etc/letsencrypt:/etc/letsencrypt
      - ./html:/var/www/html
    command: certonly --webroot -w /var/www/html -d example.com --email admin@example.com --agree-tos --non-interactive
```

---

## 8. Dépannage Avancé <a name="depannage"></a>

### Commandes de diagnostic

```bash
# Vérification du certificat
sudo certbot certificates

# Test de connexion SSL
openssl s_client -connect example.com:443 -servername example.com

# Vérification de la chaîne de certificats
openssl s_client -connect example.com:443 -showcerts

# Test OCSP Stapling
openssl s_client -connect example.com:443 -status

# Analyse SSL avec sslabs
# Visiter: https://www.ssllabs.com/ssltest/
```

### Script de monitoring santé SSL

```bash
#!/bin/bash
# ssl-health-check.sh

DOMAIN="example.com"
DAYS_WARNING=30
CERT_FILE="/etc/letsencrypt/live/$DOMAIN/fullchain.pem"

# Vérification de l'expiration
EXPIRY_DATE=$(openssl x509 -in $CERT_FILE -noout -enddate | cut -d= -f2)
EXPIRY_EPOCH=$(date -d "$EXPIRY_DATE" +%s)
CURRENT_EPOCH=$(date +%s)
DAYS_LEFT=$(( (EXPIRY_EPOCH - CURRENT_EPOCH) / 86400 ))

if [ $DAYS_LEFT -lt $DAYS_WARNING ]; then
    echo "ALERTE: Le certificat SSL pour $DOMAIN expire dans $DAYS_LEFT jours"
    # Notification ou action corrective
fi

# Vérification de la configuration Nginx
nginx -t 2>&1 | grep -q "test is successful"
if [ $? -ne 0 ]; then
    echo "ERREUR: Configuration Nginx invalide"
    exit 1
fi

echo "Statut SSL: OK ($DAYS_LEFT jours restants)"
```

### Gestion des erreurs courantes

```bash
# Erreur: Too many registrations
# Solution: Utiliser --register-unsafely-without-email

# Erreur: Rate limit exceeded
# Solution: Attendre la fin de la période ou utiliser un staging environment

# Erreur: Challenge failed
# Solution: Vérifier l'accessibilité du domaine sur le port 80/443

# Mode staging pour tests
sudo certbot --staging --nginx -d example.com
```

### Configuration de secours

```nginx
# Serveur de secours en cas d'échec SSL
server {
    listen 80;
    server_name example.com;
    
    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }
    
    location / {
        return 301 https://$host$request_uri;
    }
}

server {
    listen 443 ssl;
    server_name example.com;
    
    # Certificat auto-signé en secours
    ssl_certificate /etc/ssl/certs/self-signed.crt;
    ssl_certificate_key /etc/ssl/private/self-signed.key;
    
    # Page de maintenance
    root /var/www/maintenance;
    index index.html;
}
```

---

## Conclusion

Ce cours couvre l'ensemble du processus de gestion SSL/TLS avec Let's Encrypt, Certbot et Nginx, depuis les bases jusqu'aux configurations professionnelles. La clé pour maintenir une infrastructure SSL sécurisée réside dans :

1. **L'automatisation** des renouvellements
2. **La surveillance** proactive des certificats
3. **L'application** des meilleures pratiques de sécurité
4. **La documentation** des procédures

N'oubliez pas de tester régulièrement vos configurations et de rester informé des évolutions des standards de sécurité.