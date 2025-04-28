# Docker init Pratique

# 🚀 ÉTAPE 1 : Créer ton application Flask simple

Connecte-toi sur ton EC2 :

```bash
ssh -i ton_fichier.pem ec2-user@IP_DE_TON_EC2
```

Puis :

```bash
mkdir flask-app
cd flask-app
```

Maintenant, crée ton fichier principal :

```bash
nano app.py
```

Copie ce code minimal dans `app.py` :

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, Docker on EC2!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

✏️ Sauvegarde et quitte (`Ctrl + O`, `Entrée`, puis `Ctrl + X`).

---

# 🚀 ÉTAPE 2 : Créer un fichier `requirements.txt`

Toujours dans le dossier `flask-app` :

```bash
nano requirements.txt
```

Ajoute dedans :

```
flask
```

C'est pour que Docker sache quelles dépendances installer.

---

# 🚀 ÉTAPE 3 : Initialiser Docker (`docker init`)

Maintenant, tape :

```bash
docker init
```

➔ Docker va détecter que tu as un projet Python et va te poser des questions :

1. **Language detected** : Python ➔ tu choisis Python.
2. **Entrypoint** : il va détecter `app.py`.
3. **Port** : tu indiques `5000`.
4. **Créer un `docker-compose.yml`** : tu peux dire **non** pour rester simple.

Docker va te créer automatiquement :
- un `Dockerfile`
- un `.dockerignore`

✅ Tu peux vérifier :

```bash
ls
```
Tu devrais voir :
```
Dockerfile  app.py  requirements.txt  .dockerignore
```

---

# 🚀 ÉTAPE 4 : Construire ton image Docker

On construit l'image :

```bash
docker build -t flask-app .
```

Explication rapide :
- `docker build` ➔ construit une image Docker.
- `-t flask-app` ➔ donne un nom à ton image.

---

# 🚀 ÉTAPE 5 : Lancer ton conteneur Docker

Une fois l'image construite, lance ton application :

```bash
docker run -d -p 5000:5000 flask-app
```

Explication rapide :
- `-d` ➔ démarre en mode "détaché" (en arrière-plan).
- `-p 5000:5000` ➔ connecte le port de ton EC2 au port de ton conteneur.

---

# 🚀 ÉTAPE 6 : Tester dans ton navigateur

Sur ton navigateur, tape :

```bash
http://IP_DE_TON_EC2:5000
```

Et tu devrais voir :

```
Hello, Docker on EC2!
```

🥳 Bravo, tu as créé une application Flask **dockerisée** sur ton **instance EC2** !

---

# 📚 Résumé Visuel

```bash
# 1. Créer app.py et requirements.txt
# 2. docker init
# 3. docker build -t flask-app .
# 4. docker run -d -p 5000:5000 flask-app
# 5. Accéder à l'IP:5000
```

