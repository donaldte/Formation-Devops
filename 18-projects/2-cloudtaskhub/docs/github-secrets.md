````markdown
# 🔐 Configuration des Variables & Secrets GitHub Actions

Ce projet utilise **GitHub Actions** pour :

- la CI (tests, build, scan, push Docker)
- la CD (déploiement automatique sur Docker Swarm)
- les notifications Slack
- les rollbacks

Pour que tout fonctionne, il faut configurer plusieurs **secrets GitHub**.

---

## 🧾 Liste des Secrets à créer

| Nom du secret            | Obligatoire | Description |
|--------------------------|------------|-------------|
| `DOCKERHUB_USERNAME`     | ✅         | Nom d’utilisateur Docker Hub utilisé pour pousser les images. |
| `DOCKERHUB_TOKEN`        | ✅         | Personal Access Token Docker Hub avec droits `read/write`. |
| `SERVER_HOST`            | ✅         | Adresse IP ou nom de domaine du serveur Docker Swarm (prod). |
| `SERVER_USER`            | ✅         | Utilisateur SSH pour se connecter au serveur (ex: `ubuntu`, `root`). |
| `SERVER_SSH_KEY`         | ✅         | **Clé privée SSH** (format PEM) permettant à GitHub Actions de se connecter au serveur. |
| `SLACK_WEBHOOK_URL`      | ✅         | URL du webhook Slack pour recevoir les notifications CI/CD. |

> 🔁 Plus tard tu pourras ajouter : `SONAR_TOKEN`, `SMTP_*`, etc. si tu réactives SonarQube ou l’email.

---

## ⚙️ 1. Créer les Secrets dans GitHub (Étape par étape)

1. Va sur ton repo GitHub :  
   👉 `https://github.com/<ton-user>/<ton-repo>`

2. Clique sur l’onglet **Settings**.

3. Dans le menu de gauche, clique sur :  
   **Security → Secrets and variables → Actions**

4. Clique sur le bouton **“New repository secret”**.

5. Pour chaque secret de la liste ci-dessus :
   - **Name** → le nom EXACT (ex: `DOCKERHUB_USERNAME`)
   - **Secret** → la valeur
   - Clique sur **Add secret**

Répète pour tous :

- `DOCKERHUB_USERNAME`
- `DOCKERHUB_TOKEN`
- `SERVER_HOST`
- `SERVER_USER`
- `SERVER_SSH_KEY`
- `SLACK_WEBHOOK_URL`

---

## 🐳 2. Générer le token Docker Hub (`DOCKERHUB_TOKEN`)

1. Connecte-toi sur Docker Hub :  
   👉 https://hub.docker.com/

2. Clique sur ton avatar en haut à droite → **Account Settings**.

3. Va dans l’onglet **Security** → **New Access Token**.

4. Donne un nom (ex: `cloudtaskhub-ci`).

5. Scope / Permissions :  
   - coche au minimum `Read & Write` sur les images.

6. Clique sur **Generate** → copie le token immédiatement.

7. Va sur GitHub → crée le secret :  

   - `DOCKERHUB_USERNAME` = ton login Docker Hub (ex: `donaldprogrammeur`)  
   - `DOCKERHUB_TOKEN` = le token que tu viens de générer  

---

## 🔑 3. Générer la clé SSH pour le déploiement (`SERVER_SSH_KEY`)

Tu vas créer une paire de clés SSH **spéciale pour GitHub Actions**.

### 🔹 Sur ta machine locale (Linux / macOS / WSL) :

```bash
ssh-keygen -t ed25519 -C "github-actions-deploy" -f ~/.ssh/cloudtaskhub_deploy
````

Tu obtiens deux fichiers :

* `~/.ssh/cloudtaskhub_deploy` → **clé privée**
* `~/.ssh/cloudtaskhub_deploy.pub` → **clé publique**

### 🔹 Copier la clé publique sur le serveur

En remplaçant `USER` et `SERVER_HOST` :

```bash
ssh-copy-id -i ~/.ssh/cloudtaskhub_deploy.pub USER@SERVER_HOST
```

ou manuellement :

1. `cat ~/.ssh/cloudtaskhub_deploy.pub` → copie tout le contenu.
2. Sur le serveur, ajoute cette ligne dans : `~/.ssh/authorized_keys`.

### 🔹 Ajouter la clé privée dans GitHub

1. Ouvre `~/.ssh/cloudtaskhub_deploy` avec un éditeur.
2. Copie **tout** le contenu (y compris `-----BEGIN OPENSSH PRIVATE KEY-----` … `-----END...`).
3. Va dans ton repo GitHub → **Settings → Secrets and variables → Actions**.
4. Ajoute un secret :

   * Name : `SERVER_SSH_KEY`
   * Value : contenu de la clé privée.

### 🔹 Ajouter `SERVER_HOST` et `SERVER_USER`

* `SERVER_HOST` → IP ou domaine de ton serveur (ex: `1.2.3.4` ou `swarm.mondomaine.com`)
* `SERVER_USER` → utilisateur SSH (ex: `ubuntu` sur EC2, `root` sur certains VPS)

---

## 💬 4. Créer le webhook Slack (`SLACK_WEBHOOK_URL`)

1. Va sur :
   👉 [https://api.slack.com/messaging/webhooks](https://api.slack.com/messaging/webhooks)

2. Clique sur **Create a new webhook** (ou configurer une “Incoming Webhook App”).

3. Choisis ton **workspace** Slack.

4. Choisis le **channel** où tu veux recevoir les alertes, ex :

   * `#cloudtaskhub-ci`
   * `#devops-alerts`

5. Slack te donne une URL du type :

   ```
   https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXX
   ```

6. Copie cette URL.

7. Dans GitHub → **Settings → Secrets and variables → Actions** :

   * Name : `SLACK_WEBHOOK_URL`
   * Value : l’URL Slack.

---

## ✅ 5. Résumé des Secrets & Utilisation dans les Workflows

Dans les fichiers `.github/workflows/*.yml` :

* `secrets.DOCKERHUB_USERNAME`
  → utilisé pour taguer & pousser les images.

* `secrets.DOCKERHUB_TOKEN`
  → utilisé avec `docker/login-action` pour s’authentifier sur Docker Hub.

* `secrets.SERVER_HOST`, `secrets.SERVER_USER`, `secrets.SERVER_SSH_KEY`
  → utilisés par `appleboy/ssh-action` pour :

  * se connecter au serveur
  * faire `docker stack deploy`
  * faire les rollbacks

* `secrets.SLACK_WEBHOOK_URL`
  → utilisé par `rtCamp/action-slack-notify` pour envoyer :

  * les échecs CI
  * les échecs / succès déploiement
  * les rollbacks

Tant que ces secrets sont correctement configurés, la CI/CD tourne **sans intervention manuelle**.

---

## 🔍 6. Vérifier que tout fonctionne

1. Fais un petit commit sur une branche `feature/*`
   → la pipeline **CI - PR** doit s’exécuter.

2. Ouvre une Pull Request vers `main` :

   * Tu dois voir la CI passer (ou échouer avec logs).
   * Si échec, un message doit arriver dans Slack.

3. Merge la PR (ou active l’auto-merge) :

   * La pipeline **CI - Main** ⇒ build/push Docker Hub
   * Puis **CD - Deploy** ⇒ déploiement sur ton serveur
   * Slack doit afficher : ✅ DEPLOY SUCCESS ou 🚨 DEPLOY FAILED.

Si tout ça fonctionne, tes secrets sont bien configurés 💪

