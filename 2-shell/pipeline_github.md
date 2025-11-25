# Mise en Place d'un Pipeline avec GitHub Actions pour Déployer une Application Django sur un VPS (AWS EC2)

## Introduction

Bienvenue dans ce cours détaillé sur l'utilisation de **GitHub Actions** pour automatiser un pipeline (Continuous Integration / Continuous Deployment) dédié au déploiement d'une application Django. GitHub Actions est une plateforme puissante intégrée à GitHub qui permet d'automatiser des workflows de développement, tels que les tests automatisés, les builds, et les déploiements sur des serveurs distants comme un VPS (Virtual Private Server) ou une VM (Virtual Machine) sur AWS EC2.

### Pourquoi GitHub Actions pour CI/CD ?
- **Automatisation** : Élimine les tâches manuelles répétitives, réduit les erreurs humaines et accélère les cycles de développement.
- **Intégration native** : Fonctionne directement avec votre dépôt GitHub, sans outils externes complexes.
- **Flexibilité** : Supporte des langages comme Python/Django, et des déploiements sur divers environnements (VPS, cloud, Docker).
- **Sécurité** : Utilise des secrets pour gérer les clés sensibles (SSH, mots de passe DB).
- **Coût** : Gratuit pour les dépôts publics ; quotas généreux pour les privés.


### Objectifs du Cours
- Comprendre et configurer un workflow GitHub Actions pour tester et déployer une app Django.
- Configurer un serveur VPS (AWS EC2) pour héberger l'app.
- Gérer les connexions sécurisées via SSH.
- Intégrer une base de données PostgreSQL via Docker.
- Ajouter des notifications pour monitorer le pipeline.
- Vérifier et déboguer le déploiement.

---

## 1. Préparation de l'Environnement : Avoir une Application Django Prête

Avant de plonger dans GitHub Actions, assurez-vous d'avoir une application Django opérationnelle localement. Cela évite les frustrations pendant le déploiement.

### Étapes Détaillées
1. **Vérifiez votre App Localement** :
   - Naviguez dans le dossier de votre projet : `cd mon_projet_django`.
   - Créez un environnement virtuel si pas déjà fait : `python -m venv venv` et activez-le (`source venv/bin/activate` sur Linux/macOS, `venv\Scripts\activate` sur Windows).
   - Installez les dépendances : `pip install -r requirements.txt`.
   - Appliquez les migrations : `python manage.py migrate`.
   - Lancez le serveur : `python manage.py runserver`.
   - Testez via navigateur (http://127.0.0.1:8000). Assurez-vous que les vues, modèles et tests fonctionnent.

2. **Poussez la Dernière Version sur GitHub** :
   - Ajoutez et commitez : `git add . && git commit -m "Préparation pour CI/CD"`.
   - Poussez : `git push origin master`.
   - Vérifiez sur GitHub que le dépôt est à jour (fichiers comme `manage.py`, `requirements.txt`, `settings.py` présents).

---

## 2. Acquisition et Configuration d'un Serveur VPS (AWS EC2)

Pour déployer, vous avez besoin d'un serveur distant. Nous utilisons AWS EC2 (gratuit pour starters), mais cela s'applique à tout VPS (DigitalOcean, Linode).

### Étapes Détaillées
1. **Créez un Compte AWS et Lancez une Instance EC2** :
   - Allez sur [aws.amazon.com](https://aws.amazon.com) et créez un compte (carte crédit requise, mais free tier couvre ~750h/mois pour t2.micro).
   - Dans la console AWS > EC2 > "Launch Instance".
   - Choisissez AMI : Amazon Linux 2023 (ou Ubuntu 22.04 pour simplicité).
   - Type d'instance : t2.micro (1 vCPU, 1GB RAM, gratuit).
   - Clés SSH : Créez une paire (mais nous en générerons une custom plus tard ; ignorez pour l'instant).
   - Stockage : 8-30GB EBS (gratuit).
   - Sécurité : Ouvrez ports 22 (SSH), 80/443 (HTTP/HTTPS), et le port 8000 pour servir notre application.
   - Lancez l'instance. Notez l'IP publique (e.g., 3.123.45.67).

2. **Connectez-vous Initialement au Serveur** :
   - Utilisez la clé AWS par défaut : `ssh -i "key.pem" ec2-user@IP` (pour Amazon Linux) ou `ubuntu@IP` (Ubuntu).
   - Mettez à jour : `sudo apt update && sudo apt upgrade -y` (Ubuntu).

3. **Installez les Paquets Nécessaires sur le Serveur** :
   - Connectez-vous via SSH.
   - Installez Python, venv, libs système, Git, Docker, etc.
     ```
     sudo apt update
     sudo apt install -y python3 python3-venv python3-pip git curl wget software-properties-common
     sudo apt install -y libpq-dev build-essential  # Pour PostgreSQL et compilation
     # Installez Docker
     curl -fsSL https://get.docker.com -o get-docker.sh
     sudo sh get-docker.sh
     sudo usermod -aG docker $USER  # Ajoutez user à groupe Docker
     newgrp docker  # Appliquez sans logout
     # Vérifiez : docker --version
     ```
   - **Explication** : Python3 pour Django ; venv pour isolation ; libpq-dev pour psycopg2 (driver Postgres) ; Git pour cloner ; Docker pour DB conteneurisée.

4. **Changez les Permissions et Propriétaires** :
   - Créez un dossier pour l'app : `sudo mkdir -p /var/www/mon-app-django && sudo chown $USER:$USER /var/www/mon-app-django`.
   - Permissions : `sudo chmod 755 /var/www/` (exécutable pour web server).
   - **Explication** : Assure que votre user (non-root) peut écrire/cloner sans sudo constant.


---

## 3. Génération et Configuration des Clés SSH pour Connexion Sécurisée

Pour que GitHub Actions puisse se connecter au serveur sans mot de passe, générez une paire de clés SSH (préférez Ed25519 à RSA pour sécurité/modernité).

### Étapes Détaillées
1. **Générez la Paire de Clés Localement** :
   - Dans votre terminal local (pas sur le serveur) :
     ```
     ssh-keygen -t ed25519 -C "votre-email@example.com"
     ```
   - **Explication Ligne par Ligne** :
     - `ssh-keygen` : Outil OpenSSH pour générer des clés.
     - `-t ed25519` : Type d'algorithme (Ed25519 : rapide, sécurisé ; fallback RSA : `-t rsa -b 4096` si serveur ancien).
     - `-C "email"` : Commentaire pour identifier la clé (utilisez votre email GitHub).
   - Appuyez sur Entrée pour chemin par défaut (`~/.ssh/id_ed25519` et `id_ed25519.pub`). Pas de passphrase pour CI (automatisation), mais ajoutez-en pour usage personnel.
   - Fichiers générés : `id_ed25519` (privée), `id_ed25519.pub` (publique).

2. **Installez la Clé Publique sur le Serveur** :
   - Copiez la publique : `cat ~/.ssh/id_ed25519.pub`.
   - Sur le serveur (via SSH initial) : `mkdir -p ~/.ssh && chmod 700 ~/.ssh`.
   - Ajoutez : `cat id_ed25519.pub >> ~/.ssh/authorized_keys` (collez le contenu copié).
   - Permissions : `chmod 600 ~/.ssh/authorized_keys`.
   - **Explication** : `authorized_keys` stocke les clés publiques autorisées. `>>` ajoute sans écraser.

3. **Stockez la Clé Privée dans GitHub Secrets** :
   - Copiez le contenu de `id_ed25519` (entier, incluant `-----BEGIN OPENSSH PRIVATE KEY-----`).
   - Dans GitHub > Repo > Settings > Secrets and variables > Actions > New repository secret.
   - Nom : `VPS_SSH_KEY` ; Valeur : Contenu de la clé privée.
   - Ajoutez aussi : `VPS_IP` (IP du serveur), `VPS_USER` (e.g., `ubuntu` ou `ec2-user`).

4. **Testez la Connexion depuis Votre Machine Locale** :
   - `ssh -i ~/.ssh/id_ed25519 VPS_USER@VPS_IP`.
   - Si succès : "Bienvenue sur Ubuntu". À ce stade, GitHub peut aussi se connecter via la clé.

---

## 4. Configuration du Workflow GitHub Actions (.github/workflows/cicd.yml)

Créez le fichier `.github/workflows/cicd.yml` dans votre repo. Copiez-collez l'exemple ci-dessous, adapté et détaillé. Ce workflow a deux jobs : `test` (CI) et `deploy` (CD).

### Exemple Complet de Workflow YAML
```yaml
name: CI/CD Pipeline for Django App

on:
  push:
    branches:
      - master

concurrency:
  group: ${{ github.ref_name }}
  cancel-in-progress: true

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_USER: test_user
          POSTGRES_PASSWORD: test_pass
          POSTGRES_DB: test_db
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready -U test_user
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Pour git log complet

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
          cache: 'pip'  # Cache des dépendances

      - name: Install Dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Run Tests
        run: |
          python manage.py test --verbosity=2 | tee test_report.txt
        env:
          DATABASE_URL: postgresql://test_user:test_pass@localhost:5432/test_db

      - name: Upload Test Report
        uses: actions/upload-artifact@v4
        with:
          name: test-report
          path: test_report.txt

      - name: Set Deployment Details
        run: |
          echo "COMMIT_HASH=$(git log -1 --pretty=format:'%h')" >> $GITHUB_ENV
          echo "DATE=$(date)" >> $GITHUB_ENV
          echo "EMAIL=$(git log -1 --pretty=format:'%ae')" >> $GITHUB_ENV

      - name: Send Email Notification (Failure)
        if: failure()
        continue-on-error: true
        uses: dawidd6/action-send-mail@v4
        with:
          server_address: smtp.gmail.com
          server_port: 587
          username: ${{ secrets.EMAIL_USERNAME }}
          password: ${{ secrets.EMAIL_PASSWORD }}
          subject: "❌ Échec des Tests CI/CD - Django App"
          to: "team@example.com, ${{ env.EMAIL }}"
          from: "CI/CD Pipeline"
          body: |
            Bonjour,

            Les tests ont échoué sur la branche master.
            Commit: ${{ env.COMMIT_HASH }}
            Date: ${{ env.DATE }}
            Auteur: ${{ env.EMAIL }}
            Repository: ${{ github.repository }}

            Consultez le rapport joint pour détails.

            L'équipe DevOps
          attachments: test_report.txt

  deploy:
    needs: test
    runs-on: ubuntu-latest

    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Setup SSH Key
        run: |
          mkdir -p ~/.ssh
          echo "${{ secrets.VPS_SSH_KEY }}" > ~/.ssh/id_ed25519
          chmod 600 ~/.ssh/id_ed25519
          ssh-keyscan -H ${{ secrets.VPS_IP }} >> ~/.ssh/known_hosts

      - name: Debug SSH Connection
        run: ssh -i ~/.ssh/id_ed25519 -o ServerAliveInterval=60 -o ServerAliveCountMax=10 ${{ secrets.VPS_USER }}@${{ secrets.VPS_IP }} "echo '✅ Connexion SSH réussie'"

      - name: Deploy to VPS
        run: |
          ssh -i ~/.ssh/id_ed25519 ${{ secrets.VPS_USER }}@${{ secrets.VPS_IP }} << 'EOF'
            cd /var/www/mon-app-django
            git pull origin master
            source venv/bin/activate
            pip install -r requirements.txt
            python manage.py migrate
            python manage.py collectstatic --noinput
            python manage.py runserver 8000
            echo "✅ Déploiement terminé !"
          EOF

      - name: Set Deployment Details
        run: |
          echo "COMMIT_HASH=$(git log -1 --pretty=format:'%h')" >> $GITHUB_ENV
          echo "DATE=$(date)" >> $GITHUB_ENV
          echo "EMAIL=$(git log -1 --pretty=format:'%ae')" >> $GITHUB_ENV

      - name: Send Email Notification (Success)
        if: success()
        continue-on-error: true
        uses: dawidd6/action-send-mail@v4
        with:
          server_address: smtp.gmail.com
          server_port: 587
          username: ${{ secrets.EMAIL_USERNAME }}
          password: ${{ secrets.EMAIL_PASSWORD }}
          subject: "✅ Déploiement Réussi - Django App"
          to: "team@example.com, ${{ env.EMAIL }}"
          from: "CI/CD Pipeline"
          body: |
            Bonjour,

            Déploiement réussi sur master !
            Commit: ${{ env.COMMIT_HASH }}
            Date: ${{ env.DATE }}
            Auteur: ${{ env.EMAIL }}
            Repository: ${{ github.repository }}

            L'app est live. Merci !

            L'équipe DevOps
```

### Explication Détaillée Ligne par Ligne et Sections

#### Nom du Workflow
```yaml
name: CI/CD Pipeline for Django App
```
- **Quoi** : Nom affiché dans l'UI GitHub Actions.
- **Pourquoi** : Clair et descriptif. **Variation** : `name: Deploy Django to EC2` pour dynamique.

#### Déclencheurs (Triggers)
```yaml
on:
  push:
    branches:
      - master
```
- **Explication Ligne par Ligne** 
  - `on:` : Section des événements.
  - `push:` : Sur push Git (merge PR, commit direct).
  - `branches: - master` : Filtre à la branche master.

- **Variations** :
  - PR : `pull_request` pour tester PRs.
  - Schedule : `schedule: - cron: '0 0 * * 0'` (hebdo dimanche minuit UTC) pour déploiements périodiques.
  - Multi-événements : `on: [push, pull_request]`.
  - Ignorer : `branches-ignore: ['develop']` pour dev branches.

#### Gestion de la Concurrence
```yaml
concurrency:
  group: ${{ github.ref_name }}
  cancel-in-progress: true
```
- **Explication**  : `group:` utilise le nom de branche pour grouper ; `cancel-in-progress: true` annule vieux runs (évite conflits deploy).
- **Contenu Ajouté** : Pour Django, utile si tests/deploy longs (~5-10min).
- **Variations** : `group: ci-${{ github.workflow }}-${{ github.ref }}` pour plus granulaire. `false` pour queue (sécurisé mais lent).
- **Astuce** : Ajoutez `permissions: { contents: read }` au top pour sécurité (limite accès).

#### Jobs : Test
- `runs-on: ubuntu-latest` : VM Ubuntu (rapide, gratuit).
- Services : Postgres Docker pour tests DB (image 16 pour modernité ; env pour creds ; ports mapping ; health checks pour fiabilité).
- Steps :
  - **Checkout** : `v4` (mise à jour 2025) ; `fetch-depth: 0` pour historique.
  - **Python Setup** : `v4` ; cache pip pour vitesse (hash sur `requirements.txt`).
  - **Install** : Upgrade pip ; install sans venv (pour CI simple ; venv optionnel).
  - **Tests** : `manage.py test` avec DB URL ; `tee` pour rapport.
  - **Upload Artifact** : Pour télécharger rapport en cas d'échec.
  - **Set Details** : Vars pour emails ; utilise Git context.
  - **Email Failure** : Action v4 ; body dynamique ; to inclut auteur ; attachment rapport. Ajoutez secrets `EMAIL_USERNAME/PASSWORD` (Gmail app password).

- **Contenu Ajouté** : Ajoutez linting : `- name: Lint run: pip install flake8 && flake8 .`.
- **Variations** : Matrix pour Python versions : `strategy: matrix: { python-version: [3.9, 3.10] }`.
- **Dépannage** : Tests fail ? Vérifiez `DATABASES` dans settings.py pour test DB.

#### Jobs : Deploy (CD)
- `needs: test` : Attends succès tests.
- Steps :
  - Checkout/SSH Setup : Clé Ed25519 ; keyscan pour known_hosts.
  - Debug SSH : Test connexion ; ajoute logs.
  - **Deploy** : SSH heredoc (`<< 'EOF'`) ; git pull, activate venv (assume venv existe sur serveur), migrate, collectstatic, lancer le service.
  - Set Details/Emails : Similaire ; success email sans attachment.

Poussez le YAML : `git add .github/workflows/cicd.yml && git commit -m "feat: Ajout CI/CD" && git push`. Vérifiez dans Actions tab.

---

## 5. Configuration Côté Serveur : Virtual Env, .env et Base de Données PostgreSQL

Après workflow, configurez le serveur manuellement (premier deploy) ou via script.

### Étapes Détaillées
1. **Clonez le Projet sur le Serveur** :
   - SSH : `cd /var/www/ && git clone git@github.com:username/repo.git mon-app-django && cd mon-app-django`.
   - **Explication** : Utilise SSH GitHub (ajoutez clé publique GitHub à repo deploy keys si besoin).

2. **Créez l'Environnement Virtuel** :
   - `python3 -m venv venv`.
   - Activez : `source venv/bin/activate`.
   - Installez : `pip install -r requirements.txt`.
   - **Explication** : Isolation ; persiste pour deploys futurs.

3. **Créez un Fichier .env pour Configuration Serveur** :
   - `nano .env` :
     ```
     DATABASE_URL=postgresql://myuser:mypassword@localhost:5432/mydatabase
     ```

4. **Setup PostgreSQL via Docker** :
   - Commande (comme dans résumé) :
     ```
     sudo docker run --name postgres16 \
       -e POSTGRES_USER=myuser \
       -e POSTGRES_PASSWORD=mypassword \
       -e POSTGRES_DB=mydatabase \
       -p 5432:5432 \
       -d postgres:16
     ```
   - **Explication Ligne par Ligne** :
     - `sudo docker run` : Lance conteneur.
     - `--name postgres16` : Nom pour `docker stop/start`.
     - `-e` : Vars env pour init DB.
     - `-p 5432:5432` : Map port host:conteneur.
     - `-d` : Démon (background).
     - `postgres:16` : Image officielle (2025 : version LTS).
   - Persist data : Ajoutez `-v /var/lib/postgresql/data:/var/lib/postgresql/data` pour volume.
   - Vérifiez : `docker ps` ; `docker logs postgres16`.

5. **Intégrez à Django** :
   - `source venv/bin/activate`.
   - Test : `python manage.py migrate` (utilise .env DB_URL).


### Variations
- Sans Docker : `sudo apt install postgresql` et configurez manuellement.
- Cloud DB : AWS RDS pour scalabilité (changez DB_URL).

---

## 6. Vérification et Tests du Déploiement

1. **Testez le Workflow** :
   - Poussez un changement mineur : `git commit -m "Test deploy" && git push`.
   - Surveillez Actions tab : Vérifiez logs steps ; téléchargez artifacts si fail.


Bravo pour ce setup complet ! 🚀