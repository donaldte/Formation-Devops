#!/bin/bash

echo "🚀 Mise à jour du système..."
sudo dnf update -y

echo "🚀 Installation des paquets nécessaires..."
sudo dnf install -y yum-utils curl gnupg2 ca-certificates lsb-release

echo "🚀 Ajout du dépôt Docker officiel..."
sudo dnf config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo

echo "🚀 Installation de Docker Engine..."
sudo dnf install -y docker-ce docker-ce-cli containerd.io

echo "🚀 Démarrage et activation de Docker..."
sudo systemctl start docker
sudo systemctl enable docker

echo "✅ Docker installé. Version :"
docker --version

echo "🚀 Installation de Docker Compose plugin..."
sudo dnf install -y docker-compose-plugin

echo "✅ Docker Compose installé. Version :"
docker compose version

echo "🚀 Installation de Nginx..."
sudo dnf install -y nginx

echo "🚀 Démarrage et activation de Nginx..."
sudo systemctl start nginx
sudo systemctl enable nginx

echo "✅ Nginx installé et en cours d'exécution. Statut :"
systemctl status nginx | grep Active

echo "🎉 Installation terminée avec succès sur Amazon Linux 2023 !"
