

# 📄 **README – Installation du Serveur VPS pour le Déploiement CloudTaskHub**

Ce guide décrit **toutes les étapes nécessaires** pour préparer un VPS pour héberger CloudTaskHub via **Docker Swarm + Traefik + CI/CD GitHub Actions**.

---

# 🚀 1. Prérequis du Serveur

* Ubuntu **20.04 / 22.04** ou Debian **11 / 12**
* Minimum **2 CPU**, **4 Go RAM**
* Un utilisateur SSH (ex : `ubuntu`, `root`)
* Un pare-feu ouvert sur :

  * **22** (SSH)
  * **80** (HTTP – Traefik)
  * **443** (HTTPS – Traefik)
  * **8080** (Traefik Dashboard – optionnel)
  * **9090** (Prometheus – optionnel)
  * **3000** (Grafana – optionnel)
  * **16686** (Jaeger – optionnel)

---

# 🧰 2. Mise à jour du serveur

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y ca-certificates curl gnupg lsb-release
```

---

# 🐳 3. Installer Docker & Docker Compose Plugin (Méthode Officielle)

## 3.1 Ajouter la clé GPG Docker

```bash
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
sudo gpg --batch --yes --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
```

## 3.2 Ajouter le dépôt Docker

```bash
echo \
  "deb [arch=$(dpkg --print-architecture) \
  signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | \
sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

## 3.3 Installer Docker

```bash
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

## 3.4 Ajouter ton utilisateur à Docker

```bash
sudo usermod -aG docker $USER
newgrp docker
```

---

# 🔧 4. Activer et vérifier Docker

```bash
sudo systemctl enable docker
sudo systemctl start docker
docker --version
docker compose version
```

---

# 🐝 5. Initialiser Docker Swarm

CloudTaskHub utilise Docker Swarm pour :

* déployer les microservices
* faire du scaling
* gérer le réseau overlay
* rolling updates
* rollback

Initialisation :

```bash
docker swarm init
```

---

# 🌐 6. Créer le réseau Traefik pour le reverse-proxy

```bash
docker network create --driver=overlay traefik-public
```

---

# 🔒 7. Protéger les certificats (acme.json)

Traefik a besoin d’un fichier ACME pour gérer les certificats HTTPS :

```bash
sudo touch /var/data/traefik/acme.json
sudo chmod 600 /var/data/traefik/acme.json
```

(Sur ton projet local : `acme.json` doit aussi exister.)

---

# 🧪 8. Installer les dépendances monitoring (Jaeger, Prometheus, Grafana)

Elles seront installées automatiquement au moment du :

```bash
docker stack deploy -c docker-compose.yml cloudtaskhub
```

Donc rien à installer ici — seulement préparer les ports dans le firewall.

---

# 🧱 9. Installer OpenSSH Server (si absent)

```bash
sudo apt install -y openssh-server
sudo systemctl enable ssh
sudo systemctl start ssh
```

---

# 🔐 10. Ajouter la clé SSH GitHub Actions (pour le déploiement)

### 10.1 Sur ton PC, tu génères :

```bash
ssh-keygen -t ed25519 -C "cloudtaskhub_deploy" -f ~/.ssh/cloudtaskhub_deploy
```

### 10.2 Copier la clé publique sur le VPS :

```bash
ssh-copy-id -i ~/.ssh/cloudtaskhub_deploy.pub USER@SERVER_IP
```

Ou manuellement :

```bash
cat ~/.ssh/cloudtaskhub_deploy.pub >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

👉 La clé **privée** va dans GitHub secret `SERVER_SSH_KEY`.

---

# 🧯 11. (OPTIONNEL) Installer Fail2Ban pour sécuriser l'accès SSH

```bash
sudo apt install fail2ban -y
```

---

# 🔥 12. (OPTIONNEL) Installer un Firewall UFW

```bash
sudo apt install ufw -y
sudo ufw allow OpenSSH
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
```

---

# 🚀 13. Déployer CloudTaskHub depuis GitHub Actions

La CD GitHub se charge de :

* se connecter en SSH
* pull les images Docker Hub
* lancer Swarm :

```bash
docker stack deploy -c docker-compose.yml cloudtaskhub
```

Donc normalement **tu n'exécutes rien manuellement après setup**.

---

# 🧹 14. Maintenance du serveur

Afficher les logs des services (exemple : gateway) :

```bash
docker service logs -f cloudtaskhub_gateway-service
```

Voir les stacks :

```bash
docker stack ls
docker stack ps cloudtaskhub
docker stack services cloudtaskhub
```

Pruner (attention !) :

```bash
docker system prune -af
```

---

# 🧭 15. URLs utiles une fois le projet déployé

| Service           | URL                                                            |
| ----------------- | -------------------------------------------------------------- |
| Gateway           | [http://gateway.localhost](http://gateway.localhost)           |
| Auth              | [http://auth.localhost](http://auth.localhost)                 |
| Project           | [http://project.localhost](http://project.localhost)           |
| Billing           | [http://billing.localhost](http://billing.localhost)           |
| Notification      | [http://notification.localhost](http://notification.localhost) |
| Analytics         | [http://analytics.localhost](http://analytics.localhost)       |
| Traefik Dashboard | http://VPS_IP:8080                                             |
| Prometheus        | http://VPS_IP:9090                                             |
| Grafana           | http://VPS_IP:3000                                             |
| Jaeger            | http://VPS_IP:16686                                            |

---

# 🎉 Conclusion

Ton VPS est maintenant prêt à :

* recevoir les déploiements GitHub Actions
* exécuter une stack microservices complète
* monitorer l’activité
* faire du tracing distribué
* supporter Kafka et Traefik
* héberger un environnement DevOps **niveau entreprise**

