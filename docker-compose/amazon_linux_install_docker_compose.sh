#!/bin/bash

echo "🚀 Mise à jour du système..."
sudo dnf update -y

echo "🚀 Installation de Docker..."
sudo dnf install -y docker
sudo systemctl start docker
sudo systemctl enable docker
echo "✅ Docker installé :"
docker --version

echo "🚀 Installation de Docker Compose (manuel)..."
sudo curl -L "https://github.com/docker/compose/releases/download/v2.24.2/docker-compose-linux-x86_64" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
echo "✅ Docker Compose installé :"
docker-compose version

echo "🚀 Installation de Nginx..."
sudo dnf install -y nginx
sudo systemctl start nginx
sudo systemctl enable nginx
echo "✅ Nginx installé et en cours d'exécution :"
systemctl status nginx | grep Active

echo "🎉 Tout a été installé avec succès sur Amazon Linux 2023 !"
