#!/bin/bash

echo "🚀 Mise à jour du système..."
sudo apt update && sudo apt upgrade -y

echo "🚀 Installation des paquets nécessaires..."
sudo apt install apt-transport-https ca-certificates curl software-properties-common -y

echo "🚀 Ajout de la clé GPG officielle de Docker..."
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

echo "🚀 Ajout du dépôt Docker à APT sources..."
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

echo "🚀 Installation de Docker Engine..."
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io -y

echo "✅ Docker installé. Version :"
docker --version

echo "🚀 Installation de Docker Compose plugin..."
sudo apt install docker-compose-plugin -y

echo "✅ Docker Compose installé. Version :"
docker compose version

echo "🚀 Installation de Nginx..."
sudo apt install nginx -y

echo "🚀 Démarrage et activation de Nginx..."
sudo systemctl start nginx
sudo systemctl enable nginx

echo "✅ Nginx installé et en cours d'exécution. Statut :"
systemctl status nginx | grep Active

echo "🚀 Configuration du pare-feu pour Nginx (si UFW est actif)..."
if sudo ufw status | grep -q "Status: active"; then
    sudo ufw allow 'Nginx Full'
    sudo ufw reload
    echo "✅ Pare-feu configuré pour Nginx."
else
    echo "⚠️ UFW n'est pas actif. Pare-feu non configuré."
fi

echo "🎉 Installation terminée avec succès !"
