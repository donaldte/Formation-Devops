
# 🖥️ Cours Complet sur le **Bash Shell Scripting**


## 1. Introduction

* **Bash** = Bourne Again SHell (interpréteur de commandes le plus courant sous Linux/Unix).
* **Shell Scripting** = écriture de scripts automatisant des tâches répétitives.
* **Utilisation en DevOps** :

  * Automatiser des déploiements (CI/CD).
  * Sauvegardes et monitoring.
  * Gestion des logs et services.
  * Intégration avec Docker, Kubernetes, Ansible, etc.

---

## 2. Premier script

Créer un fichier `hello.sh` :

```bash
#!/bin/bash
echo "Hello, DevOps World!"
```

* Rendre exécutable :

```bash
chmod +x hello.sh
./hello.sh
```

---

## 3. Variables

### Déclaration et utilisation

```bash
NAME="Donald"
echo "Bonjour $NAME"
```

### Variables spéciales

* `$0` : nom du script
* `$1, $2, ...` : arguments passés
* `$#` : nombre d’arguments
* `$@` : tous les arguments
* `$?` : code retour de la dernière commande

Exemple :

```bash
#!/bin/bash
echo "Script: $0"
echo "Premier argument: $1"
echo "Nombre d'arguments: $#"
```

---

## 4. Lecture utilisateur

```bash
#!/bin/bash
read -p "Quel est ton nom ? " NOM
echo "Bonjour $NOM !"
```

---

## 5. Conditions (if/else)

```bash
#!/bin/bash
if [ -f "/etc/passwd" ]; then
  echo "Le fichier existe"
else
  echo "Fichier introuvable"
fi
```

* Comparaisons numériques :

  * `-eq`, `-ne`, `-gt`, `-lt`, `-ge`, `-le`
* Comparaisons de chaînes :

  * `=`, `!=`, `-z` (vide), `-n` (non vide)

---

## 6. Boucles

### For

```bash
for i in 1 2 3; do
  echo "Iteration $i"
done
```

### While

```bash
COUNT=1
while [ $COUNT -le 5 ]; do
  echo "Compteur: $COUNT"
  COUNT=$((COUNT+1))
done
```

### Until

```bash
until [ $COUNT -eq 10 ]; do
  echo "COUNT=$COUNT"
  COUNT=$((COUNT+1))
done
```

---

## 7. Fonctions

```bash
ma_fonction() {
  echo "Hello depuis une fonction"
}
ma_fonction
```

Avec paramètres :

```bash
hello() {
  echo "Salut $1 !"
}
hello Donald
```

---

## 8. Gestion des erreurs

```bash
#!/bin/bash
set -e   # arrêter si une erreur survient
ls /dossier_inexistant
echo "Cette ligne ne s'exécutera pas"
```

Gestion manuelle :

```bash
if ! ls /fakepath; then
  echo "Erreur détectée"
fi
```

---

## 9. Manipulation des fichiers

```bash
#!/bin/bash
FICHIER="test.txt"

if [ -e "$FICHIER" ]; then
  echo "Le fichier existe"
else
  echo "Création du fichier"
  touch $FICHIER
fi
```

---

## 10. Scripts avancés DevOps

### 10.1. Sauvegarde automatique

```bash
#!/bin/bash
DATE=$(date +%F)
tar -czf backup_$DATE.tar.gz /var/www
echo "Backup terminé"
```

### 10.2. Vérification d’un service

```bash
#!/bin/bash
SERVICE="nginx"

if systemctl is-active --quiet $SERVICE; then
  echo "$SERVICE est actif"
else
  echo "$SERVICE est arrêté"
fi
```

### 10.3. Déploiement automatisé

```bash
#!/bin/bash
echo "Pulling latest code..."
git pull origin main

echo "Restarting Docker containers..."
docker-compose down
docker-compose up -d --build

echo "Déploiement terminé 🚀"
```

---

## 11. Bonnes pratiques

* Toujours commencer par `#!/bin/bash`
* Indenter et commenter le code
* Utiliser `set -e` pour stopper en cas d’erreur
* Gérer les logs (`>> logfile.log 2>&1`)
* Modulariser avec des **fonctions**
* Préférer les scripts **idempotents** (qui ne cassent pas si relancés)

---

## 12. Exercices pratiques

1. Écrire un script qui :

   * Crée un dossier `logs/`
   * Copie les logs `/var/log/syslog` dedans
   * Les compresse avec tar et date
2. Faire un script qui **surveille un service** (nginx, mysql) toutes les 10s et envoie une alerte si le service tombe.
3. Créer un script qui supprime les fichiers temporaires plus vieux que 7 jours dans `/tmp`.
4. Écrire un mini-script d’installation automatique d’Apache/Nginx selon l’OS détecté (`apt` vs `yum`).

---

## 13. Ressources utiles

* `man bash`
* [Bash Guide for Beginners (GNU)](https://tldp.org/LDP/Bash-Beginners-Guide/html/)
* [Advanced Bash Scripting Guide](https://tldp.org/LDP/abs/html/)


