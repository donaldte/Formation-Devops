Voici la traduction complète en français :
# Docker avec des exemples. Les contributions sont les bienvenues !

## Si ce dépôt vous a été utile, laissez une ÉTOILE 🌠

Vous pouvez regarder la version vidéo de ce dépôt sur ma playlist YouTube :  
https://youtube.com/playlist?list=PLJuTqSmOxhNvPaEY54pIUvBHYR6c8uxIH&feature=shared
---

## Qu’est-ce qu’un conteneur ?

Un conteneur est une unité standard de logiciel qui regroupe du code et toutes ses dépendances, de sorte que l'application s'exécute rapidement et de manière fiable d’un environnement informatique à un autre.  
Une image de conteneur Docker est un package logiciel autonome, léger et exécutable contenant tout ce qu’il faut pour faire fonctionner une application : le code, le runtime, les outils système, les bibliothèques système et les paramètres.

Ok, simplifions !

Un conteneur est un ensemble comprenant l’application, ses bibliothèques nécessaires, et le strict minimum des dépendances système.

![Capture 1](https://user-images.githubusercontent.com/43399466/217262726-7cabcb5b-074d-45cc-950e-84f7119e7162.png)

---

## Conteneurs vs Machines Virtuelles

Les conteneurs et les machines virtuelles (VM) servent tous deux à isoler les applications et leurs dépendances, mais ils diffèrent sur plusieurs points clés :

1. **Utilisation des ressources** : Les conteneurs partagent le noyau du système hôte, ce qui les rend plus légers et plus rapides que les VM. Les VM nécessitent un OS complet et un hyperviseur, ce qui les rend plus lourdes.

2. **Portabilité** : Les conteneurs sont conçus pour être portables et fonctionner sur tout système compatible. Les VM sont moins portables car elles nécessitent un hyperviseur compatible.

3. **Sécurité** : Les VM offrent une isolation plus forte (chaque VM a son propre OS). Les conteneurs partagent le noyau de l’hôte et offrent donc une isolation moindre.

4. **Gestion** : Les conteneurs sont plus faciles à gérer car ils sont conçus pour être légers et rapides à déployer.

---

## Pourquoi les conteneurs sont-ils légers ?

Les conteneurs sont légers car ils utilisent la **containerisation**, une technologie qui leur permet de partager le noyau de l’OS hôte tout en gardant une isolation suffisante. Ils n’ont pas besoin d’un OS complet.

Prenons un exemple :

Une image Docker Ubuntu officielle ne pèse que ~22 Mo, tandis qu’une image VM Ubuntu peut peser ~2,3 Go ! Le conteneur est donc environ 100 fois plus léger.

![Capture 2](https://user-images.githubusercontent.com/43399466/217493284-85411ae0-b283-4475-9729-6b082e35fc7d.png)

---

### Fichiers et dossiers présents dans une image de base Docker :

```
/bin  : exécutables système de base (ls, cp, ps...)
/sbin : exécutables système (init, shutdown...)
/etc  : fichiers de configuration
/lib  : bibliothèques utilisées par les binaires
/usr  : applications, bibliothèques et documentation
/var  : fichiers logs, temporaires, files d’attente
/root : répertoire personnel de l'utilisateur root
```

---

### Fichiers et ressources utilisés depuis l’hôte :

```
- Système de fichiers de l’hôte (via bind mounts)
- Pile réseau de l’hôte (réseau direct ou virtuel)
- Appels système gérés par le noyau de l’hôte
- Namespaces Linux pour isoler les processus
- Cgroups pour limiter les ressources (CPU, RAM, I/O)
```

⚠️ Même si les conteneurs utilisent des ressources de l’hôte, ils restent isolés. Les changements dans un conteneur n'affectent pas l’hôte ni les autres conteneurs.

---

## Docker

### Qu’est-ce que Docker ?

Docker est une **plateforme de containerisation**. Elle permet de :

- Créer des images Docker avec `docker build`
- Lancer des conteneurs avec `docker run`
- Partager les images avec `docker push`

👉 La **containerisation** est une **technologie**. **Docker** en est une **implémentation**.

---

### Architecture de Docker

![Docker Architecture](https://user-images.githubusercontent.com/43399466/217507877-212d3a60-143a-4a1d-ab79-4bb615cb4622.png)

➡️ Le **Docker Daemon** est le cerveau de Docker. S’il s’arrête… Docker est "mort" 😅

---

### Cycle de vie Docker

Basé sur l’image ci-dessus :

1. `docker build` : crée une image à partir d’un `Dockerfile`  
2. `docker run` : exécute un conteneur à partir d’une image  
3. `docker push` : envoie l’image sur un registre public ou privé

---

### Terminologie

#### Docker Daemon (dockerd)
Écoute les requêtes de l’API Docker et gère les objets Docker (images, conteneurs, volumes, etc.).

#### Docker Client (docker)
C’est l’outil en ligne de commande pour interagir avec Docker (via l’API Docker).

#### Docker Desktop
Application pour Mac, Windows, Linux : elle embarque Docker Daemon, Client, Compose, Kubernetes, etc.

#### Registres Docker
Stockent les images Docker (ex: Docker Hub, Quay.io).  
`docker pull` pour télécharger, `docker push` pour envoyer.

#### Dockerfile
Fichier listant les étapes de construction d’une image.

#### Images
Templates en lecture seule pour créer des conteneurs.

---

## INSTALLER DOCKER

👉 Guide officiel : https://docs.docker.com/get-docker/

### Démo rapide sur une instance Ubuntu (EC2 AWS par exemple) :

```bash
sudo apt update
sudo apt install docker.io -y
```

---

### Démarrer Docker et donner les bons accès

Pour les débutants, une erreur fréquente est d’oublier de démarrer Docker et d’ajouter leur utilisateur au groupe `docker`.

Vérifiez que Docker est bien actif :

```bash
sudo systemctl status docker
```

Si ce n’est pas le cas :

```bash
sudo systemctl start docker
```

Ajouter l’utilisateur actuel au groupe docker :

```bash
sudo usermod -aG docker ubuntu
```

🔁 Déconnectez-vous puis reconnectez-vous pour que cela prenne effet.

---

### Tester votre installation Docker

```bash
docker run hello-world
```

Si vous voyez un message d’erreur :

```
permission denied /var/run/docker.sock
```

Cela signifie que Docker n’est pas lancé ou que vous n’avez pas les droits d’accès.

---

## Docker est installé et fonctionne 🥳

---

## Commencez avec les exemples

### Cloner ce dépôt et aller dans le dossier `examples`

```bash
git clone https://github.com/donaldte/Formation-Devops.git
cd docker / cd firt-project-file
```

### Se connecter à DockerHub

```bash
docker login
```

---

### Créer votre première image Docker

```bash
docker build -t votre_username/ma-premiere-image:latest .
```

---

### Vérifier que l’image est bien créée

```bash
docker images
```

---

### Exécuter votre premier conteneur

```bash
docker run -it votre_username/ma-premiere-image
```

---

### Pousser votre image sur DockerHub

```bash
docker push votre_username/ma-premiere-image
```

---

## Bravo 🎉 Vous êtes prêt à devenir un champion de Docker 💪

