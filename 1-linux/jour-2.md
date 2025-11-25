# 🐧 Cours Complet Linux pour DevOps

## Introduction

### Pourquoi Linux est incontournable pour le DevOps
- **97% des serveurs web** dans le monde utilisent Linux
- **Tous les outils DevOps majeurs** (Docker, Kubernetes, Jenkins, Terraform) fonctionnent sur Linux
- **Les conteneurs sont basés sur Linux** - même sous Windows/Mac, Docker utilise un noyau Linux virtualisé

### Rôle du shell (Bash/Zsh)
- Automatiser des tâches répétitives
- Manipuler des fichiers et processus
- Superviser des services
- Déployer des applications

---

## 1. Structure du Système de Fichiers Linux

### Hiérarchie des répertoires essentiels
```
/               → Racine du système de fichiers
├── bin/        → Commandes essentielles (ls, cp, mkdir...)
├── etc/        → Fichiers de configuration système
├── home/       → Répertoires personnels des utilisateurs
├── root/       → Répertoire de l'administrateur
├── tmp/        → Fichiers temporaires (effacés au redémarrage)
├── usr/        → Applications et programmes utilisateur
├── var/        → Fichiers variables (logs, bases de données...)
└── lib/        → Bibliothèques partagées essentielles
```

### Distributions Linux courantes en DevOps
1. **Ubuntu** - La plus populaire, excellente documentation
2. **CentOS/RHEL** - Standard en entreprise, très stable
3. **Debian** - Très stable, base d'Ubuntu
4. **Alpine Linux** - Légère, parfaite pour les conteneurs

---

## 2. Commandes Linux Essentielles

### 2.1 Navigation & gestion des fichiers
```bash
pwd          # Affiche le répertoire courant
ls -la       # Liste les fichiers avec détails et fichiers cachés
cd /chemin   # Change de répertoire
tree         # Affiche l'arborescence (à installer avec 'yum install tree' ou 'apt install tree')
```

### 2.2 Lecture et manipulation de fichiers
```bash
cat fichier.txt       # Affiche tout le contenu
less fichier.txt      # Affiche page par page (quitter avec 'q')
head -n 10 fichier.txt # Affiche les 10 premières lignes
tail -f fichier.log   # Affiche la fin et suit les nouvelles entrées (logs en temps réel)
```

### 2.3 Création, copie, suppression
```bash
touch nouveau.txt     # Crée un fichier vide
mkdir nouveau_dossier # Crée un dossier
cp source.txt dest/   # Copie un fichier
mv ancien.txt nouveau.txt # Renomme ou déplace
rm fichier.txt        # Supprime (attention! pas de corbeille)
rm -r dossier/        # Supprime récursivement
```

### 2.4 Recherche de fichiers et contenu
```bash
find /home -name "*.log"          # Trouve tous les fichiers .log dans /home
grep "ERROR" /var/log/syslog      # Cherche "ERROR" dans le fichier
grep -r "database" /etc/          # Recherche récursive dans tous les fichiers
```

---

## 3. Gestion des Utilisateurs et Permissions

### Commandes essentielles
```bash
whoami        # Affiche l'utilisateur courant
id            # Affiche les informations de l'utilisateur
sudo commande # Exécute une commande en tant que superutilisateur
```

### Gestion des permissions
```bash
chmod 755 script.sh    # Donne tous droits au propriétaire, lecture/exécution aux autres
chown user:group fichier # Change le propriétaire et le groupe
```

#### Comprendre chmod (permissions Linux)
- **Lecture (r)** = 4
- **Écriture (w)** = 2
- **Exécution (x)** = 1

Exemple: `chmod 764 fichier`
- Propriétaire: 7 (4+2+1 = rwx)
- Groupe: 6 (4+2 = rw-)
- Autres: 4 (r--)

---

## 4. Gestion des Processus et Services

### Surveillance des processus
```bash
ps aux                 # Liste tous les processus
top                    # Affiche les processus en temps réel (quitter avec 'q')
htop                   # Version améliorée de top (à installer)
```

### Gestion des services avec systemctl
```bash
systemctl status nginx    # Vérifie le statut du service
systemctl start nginx     # Démarre le service
systemctl stop nginx      # Arrête le service
systemctl restart nginx   # Redémarre le service
systemctl enable nginx    # Active le démarrage automatique
```

### Consultation des logs
```bash
journalctl -u nginx -f    # Affiche les logs de nginx en temps réel
tail -f /var/log/nginx/access.log # Suit les logs d'accès nginx
```

---

## 5. Réseau et Connectivité

### Commandes réseau essentielles
```bash
ping google.com          # Teste la connectivité
curl http://example.com  # Télécharge ou teste une URL
wget http://example.com/file.zip # Télécharge un fichier
```

### Analyse des ports et connexions
```bash
netstat -tuln            # Affiche les ports en écoute
ss -tuln                 # Version moderne de netstat
```

### Transfert de fichiers et connexion distante
```bash
scp -i clé.pem fichier.local user@server:/distant/ # Copie sécurisée
rsync -avz dossier/ user@server:/distant/          # Synchronisation efficace
ssh -i clé.pem user
```
scp -i "oui-front.pem" -r C:\Users\YourName\project-folder ubuntu@ec2-35-87-145-195.us-west-2.compute.amazonaws.com:/home/ubuntu/

scp -i "oui-front.pem" -r ubuntu@ec2-35-87-145-195.us-west-2.compute.amazonaws.com:/home/ubuntu/logs C:\Users\YourName\Downloads\

Chaque fichier/dossier a 3 types de permissions:
- **Lecture (r)** = 4 - Voir le contenu
- **Écriture (w)** = 2 - Modifier/supprimer
- **Exécution (x)** = 1 - Exécuter (fichiers) ou traverser (dossiers)

Et 3 types d'utilisateurs:
- **Propriétaire (u)** - User qui possède le fichier
- **Groupe (g)** - Groupe propriétaire du fichier
- **Autres (o)** - Tous les autres utilisateurs

### Commandes de gestion des permissions

```bash
# Afficher les permissions détaillées
ls -l fichier.txt
ls -ld dossier/    # Pour un dossier

# Changer les permissions avec chmod
chmod 755 fichier.txt          # Notation numérique
chmod u+rwx,g+rx,o+rx fichier.txt # Notation symbolique
chmod -R 755 dossier/          # Récurssif pour un dossier

# Changer le propriétaire et le groupe
chown utilisateur:fichier.txt  # Changer propriétaire et groupe
chown utilisateur fichier.txt  # Changer seulement propriétaire
chgrp groupe fichier.txt       # Changer seulement le groupe
```

### Masque umask
```bash
umask          # Affiche le masque courant (0022)
umask 002      # Change le masque
```
La permission réelle = permissions de base - umask

---

## 2. Gestion des Processus

### Visualisation des processus
```bash
ps aux                 # Tous les processus
ps -ef                 # Format étendu
top                    # Visualisation temps réel
htop                   # Version améliorée (à installer)
pstree                 # Arbre des processus
```

### Gestion et suppression des processus
```bash
kill 1234              # Terminer le processus PID 1234
kill -9 1234           # Forcer la terminaison
killall nginx          # Terminer tous les processus nginx
pkill firefox          # Terminer par nom
nice -n 10 commande    # Lancer avec priorité basse
renice 15 -p 1234      # Changer la priorité d'un processus
```

### Processus en arrière-plan
```bash
commande &             # Lancer en arrière-plan
jobs                   # Lister les jobs en arrière-plan
fg %1                  # Ramener le job 1 au premier plan
bg %1                  # Remettre le job 1 en arrière-plan
ctrl + z               # Suspendre un processus au premier plan
```

---

## 3. Gestion des Utilisateurs et Groupes

### Création et modification d'utilisateurs
```bash
# Créer un utilisateur
sudo useradd -m -s /bin/bash nouvel_utilisateur
sudo passwd nouvel_utilisateur  # Définir le mot de passe

# Modifier un utilisateur
sudo usermod -aG sudo utilisateur  # Ajouter aux groupes sudo
sudo usermod -s /bin/sh utilisateur # Changer le shell
sudo usermod -L utilisateur        # Verrouiller le compte
sudo usermod -U utilisateur        # Déverrouiller le compte

# Supprimer un utilisateur
sudo userdel -r utilisateur        # Supprimer avec son home directory
```

### Gestion des groupes
```bash
# Créer et gérer les groupes
sudo groupadd dev_group           # Créer un nouveau groupe
sudo groupmod -n new_name old_name # Renommer un groupe
sudo groupdel groupe_name         # Supprimer un groupe

# Ajouter/retirer des utilisateurs d'un groupe
sudo usermod -aG groupe utilisateur  # Ajouter au groupe
sudo gpasswd -d utilisateur groupe   # Retirer du groupe
```

### Fichiers de configuration importants
```bash
/etc/passwd    # Informations des utilisateurs
/etc/shadow    # Mots de passe chiffrés
/etc/group     # Informations des groupes
/etc/sudoers   # Configuration sudo
```

---

## 4. Exercices Pratiques

### Exercice 1: Gestion des Permissions

**Objectif**: Créer une structure sécurisée pour un projet d'équipe

```bash
# 1. Créez la structure suivante:
sudo mkdir -p /projet_equipe/{dev,prod,logs,backup}

# 2. Créez les groupes
sudo groupadd devs
sudo groupadd admins

# 3. Créez les utilisateurs
sudo useradd -m -G devs dev1
sudo useradd -m -G devs dev2
sudo useradd -m -G admins admin1

# 4. Configurez les permissions
sudo chown root:admins /projet_equipe
sudo chmod 775 /projet_equipe

sudo chown dev1:devs /projet_equipe/dev
sudo chmod 2770 /projet_equipe/dev  # sticky bit pour conservation groupe

sudo chown admin1:admins /projet_equipe/prod
sudo chmod 770 /projet_equipe/prod

# 5. Testez les accès
sudo -u dev1 touch /projet_equipe/dev/test_dev1.txt
sudo -u dev2 touch /projet_equipe/dev/test_dev2.txt
sudo -u admin1 touch /projet_equipe/prod/test_admin.txt
```

### Exercice 2: Gestion des Processus

**Objectif**: Surveiller et gérer les processus système

```bash
# 1. Lancez quelques processus de test
sleep 300 &
tail -f /var/log/syslog &
nginx  # si installé, ou utilisez un autre service

# 2. Identifiez les processus
ps aux | grep -E "sleep|tail|nginx"
pgrep sleep

# 3. Changez la priorité d'un processus
nice -n 15 sleep 200 &
renice 10 -p $(pgrep sleep)

# 4. Suspendre et reprendre un processus
# Trouvez un processus, suspendez-le avec Ctrl+Z, puis:
jobs
fg %1  # pour le ramener au premier plan
bg %1  # pour le remettre en arrière-plan

# 5. Terminez proprement les processus
pkill sleep
killall tail
```

### Exercice 3: Utilisateurs et Groupes Avancés

**Objectif**: Configurer un environnement multi-utilisateurs avec permissions spécifiques

```bash
# 1. Créez les groupes et utilisateurs
sudo groupadd developers
sudo groupadd auditors

sudo useradd -m -G developers alice
sudo useradd -m -G developers bob
sudo useradd -m -G auditors charlie

# 2. Créez la structure de directories
sudo mkdir -p /company/{projects,audit,shared}

# 3. Configurez les permissions avec ACL (Access Control Lists)
sudo setfacl -R -m g:developers:rwx /company/projects
sudo setfacl -R -m g:auditors:rx /company/projects
sudo setfacl -R -m g:auditors:rwx /company/audit
sudo setfacl -R -m g:developers:rwx /company/shared
sudo setfacl -R -m o::rx /company/shared

# 4. Vérifiez les ACL
getfacl /company/projects

# 5. Testez avec différents utilisateurs
sudo -u alice touch /company/projects/alice_file.txt
sudo -u bob touch /company/projects/bob_file.txt
sudo -u charlie ls -la /company/projects/  # Doit pouvoir lire mais pas écrire
```

### Exercice 4: Script de Surveillance Automatisée

**Objectif**: Créer un script qui surveille les processus et envoie des alertes

```bash
#!/bin/bash
# surveillance-processus.sh

SERVICES=("nginx" "mysql" "ssh")

for service in "${SERVICES[@]}"; do
    if ! pgrep -x "$service" > /dev/null; then
        echo "ALERTE: Le service $service n'est pas en cours d'exécution!"
        echo "$(date): Service $service arrêté" >> /var/log/service_monitor.log
        # systemctl restart $service  # Décommentez pour redémarrer automatiquement
    fi
done

# Surveillance de l'utilisation mémoire
MEM_USAGE=$(free | awk '/Mem:/ {printf("%.2f"), $3/$2 * 100}')
if (( $(echo "$MEM_USAGE > 90" | bc -l) )); then
    echo "ALERTE: Utilisation mémoire élevée: $MEM_USAGE%"
    echo "$(date): Mémoire élevée: $MEM_USAGE%" >> /var/log/service_monitor.log
fi
```

### Exercice 5: Configuration Sudo Avancée

**Objectif**: Donner des permissions sudo spécifiques à des utilisateurs

```bash
# 1. Créez un fichier de configuration sudo personnalisé
sudo visudo -f /etc/sudoers.d/devops-permissions

# 2. Ajoutez ces lignes (décommentez et adaptez):
# %devops ALL=(ALL) NOPASSWD: /bin/systemctl restart nginx, /bin/systemctl status nginx
# alice ALL=(ALL) NOPASSWD: /usr/bin/apt update, /usr/bin/apt upgrade

# 3. Testez les permissions
sudo -u alice sudo apt update  # Devrait fonctionner sans mot de passe
sudo -u alice sudo reboot      # Devrait échouer (permission non accordée)
```

### Exercice 6: Gestion des Permissions avec ACL

**Objectif**: Utiliser les ACL pour des permissions avancées

```bash
# 1. Installez les outils ACL si nécessaire
sudo apt install acl  # Debian/Ubuntu
sudo yum install acl  # CentOS/RHEL

# 2. Créez une structure de test
mkdir test_acl
touch test_acl/fichier.txt

# 3. Appliquez des ACL spécifiques
setfacl -m u:alice:rwx test_acl/
setfacl -m g:developers:rx test_acl/
setfacl -m u:charlie:r-- test_acl/fichier.txt

# 4. Vérifiez les ACL
getfacl test_acl/
getfacl test_acl/fichier.txt

# 5. Testez les permissions
sudo -u alice touch test_acl/test_alice.txt
sudo -u bob ls -la test_acl/      # Doit pouvoir lire
sudo -u charlie cat test_acl/fichier.txt  # Doit pouvoir lire
```

---

## 5. Bonnes Pratiques de Sécurité

1. **Principe du moindre privilège**: Donnez seulement les permissions nécessaires
2. **Utilisez des groupes** pour gérer les permissions plutôt que des utilisateurs individuels
3. **Auditez régulièrement** les permissions avec `find / -perm -4000` pour trouver les SUID
4. **Utilisez les ACL** pour des besoins de permission complexes
5. **Journalisez les actions sudo** avec `sudo tail -f /var/log/auth.log`
6. **Désactivez les comptes inutilisés**
7. **Utilisez des mots de passe forts** et changez-les régulièrement

---

## 6. Commandes de Vérification et Audit

```bash
# Vérifier les dernières connexions
last
lastlog

# Vérifier les tentatives de connexion échouées
sudo grep "Failed password" /var/log/auth.log

# Trouver les fichiers avec des permissions spéciales
find / -perm -4000 2>/dev/null  # SUID files
find / -perm -2000 2>/dev/null  # SGID files

# Vérifier les processus suspects
ps aux --sort=-%cpu | head -10  # Top 10 processus CPU
ps aux --sort=-%mem | head -10  # Top 10 processus mémoire

# Audit des permissions
ls -la /etc/passwd /etc/shadow  # Doit être root:root et 644/600
```

