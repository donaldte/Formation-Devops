# 🔥 Exercices Bash pour DevOps

---

## 1. Vérifier la disponibilité d’un site web

👉 **Énoncé**
Écrire un script qui prend en argument une URL et affiche :

* "UP ✅" si le site répond avec un code HTTP 200.
* "DOWN ❌" sinon.

### ✅ Solution

```bash
#!/bin/bash
URL=$1

if [ -z "$URL" ]; then
  echo "Usage: $0 <url>"
  exit 1
fi

STATUS=$(curl -o /dev/null -s -w "%{http_code}\n" $URL)

if [ "$STATUS" -eq 200 ]; then
  echo "$URL is UP ✅"
else
  echo "$URL is DOWN ❌ (code: $STATUS)"
fi
```

---

## 2. Backup automatique avec horodatage

👉 **Énoncé**
Écrire un script qui compresse `/var/log` dans un fichier `.tar.gz` avec la date du jour dans le nom.

### ✅ Solution

```bash
#!/bin/bash
DATE=$(date +%F_%H-%M-%S)
DEST="/backup/logs_$DATE.tar.gz"

mkdir -p /backup
tar -czf $DEST /var/log

echo "Backup créé : $DEST"
```

---

## 3. Surveillance de service (ex: nginx)

👉 **Énoncé**
Écrire un script qui vérifie si `nginx` est actif.

* Si oui → affiche `"nginx est actif ✅"`.
* Sinon → redémarre nginx et logue l’action dans `/var/log/nginx_check.log`.

### ✅ Solution

```bash
#!/bin/bash
SERVICE="nginx"
LOG="/var/log/nginx_check.log"

if systemctl is-active --quiet $SERVICE; then
  echo "$(date) - $SERVICE est actif ✅"
else
  echo "$(date) - $SERVICE est arrêté ❌ → redémarrage..." | tee -a $LOG
  systemctl start $SERVICE
fi
```

---

## 4. Nettoyage automatique des fichiers temporaires

👉 **Énoncé**
Écrire un script qui supprime tous les fichiers de `/tmp` plus vieux que 7 jours et logue les fichiers supprimés.

### ✅ Solution

```bash
#!/bin/bash
LOG="/var/log/tmp_cleanup.log"
echo "=== Nettoyage lancé à $(date) ===" >> $LOG

find /tmp -type f -mtime +7 -print -delete >> $LOG

echo "=== Fin du nettoyage ===" >> $LOG
```

---

## 5. Déploiement simple d’une application avec Git & Docker

👉 **Énoncé**
Écrire un script qui :

1. Fait un `git pull` dans `/app`.
2. Redémarre les conteneurs Docker avec `docker-compose`.
3. Écrit un message de succès.

### ✅ Solution

```bash
#!/bin/bash
APP_DIR="/app"

cd $APP_DIR || exit 1

echo "📥 Pulling latest code..."
git pull origin main

echo "🐳 Restarting Docker containers..."
docker-compose down
docker-compose up -d --build

echo "🚀 Déploiement terminé avec succès à $(date)"
```



## 6 : Nettoyer automatiquement les `/var/log` de plus d’un an avec `cron`

---

## 📌 Énoncé

* Écrire un **script Bash** qui supprime tous les fichiers de `/var/log` de plus de **365 jours**.
* Ajouter ce script dans la **crontab** pour qu’il s’exécute automatiquement **tous les dimanches à minuit**.
* Le script doit **loguer les actions** dans un fichier `/var/log/log_cleanup.log`.

---

## ✅ Solution

### 1. Écrire le script `cleanup_logs.sh`

```bash
#!/bin/bash
LOGFILE="/var/log/log_cleanup.log"
echo "=== Nettoyage lancé à $(date) ===" >> $LOGFILE

# Trouver et supprimer les logs de plus de 365 jours
find /var/log -type f -mtime +365 -print -delete >> $LOGFILE 2>&1

echo "=== Fin du nettoyage ===" >> $LOGFILE
```

* Donner les droits d’exécution :

```bash
chmod +x /usr/local/bin/cleanup_logs.sh
```

---

### 2. Créer la tâche cron

Éditer la crontab avec :

```bash
crontab -e
```

Ajouter la ligne suivante :

```bash
0 0 * * 0 /usr/local/bin/cleanup_logs.sh
```

👉 Explication :

* `0 0 * * 0` = tous les dimanches à 00h00.
* Le script sera exécuté automatiquement.

---

### 3. Vérifier la crontab

```bash
crontab -l
```

---

### 4. Vérifier les logs après exécution

Consulter le fichier :

```bash
cat /var/log/log_cleanup.log
```


