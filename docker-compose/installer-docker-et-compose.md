

# ✅ Installation de Docker Compose V2 (méthode officielle)



## 🧹 1️⃣ Supprime toute ancienne configuration incomplète

```bash
sudo rm -rf /etc/apt/keyrings/docker.gpg
sudo rm -f /etc/apt/sources.list.d/docker.list
sudo apt update
```

---

## 🧭 2️⃣ Vérifie ta version Ubuntu

C’est important car le dépôt Docker dépend de la version :

```bash
lsb_release -a
```

Tu devrais voir quelque chose comme :

```
Distributor ID: Ubuntu
Description:    Ubuntu 22.04.5 LTS
Codename:       jammy
```

➡️ Garde en tête ton **Codename** (ex: `jammy`, `focal`, `noble`, etc.)

---

## 🧱 3️⃣ Ajoute la clé GPG officielle de Docker

```bash
sudo apt install -y ca-certificates curl gnupg lsb-release
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
```

---

## 🧩 4️⃣ Ajoute le dépôt stable Docker à APT

👉 Remplace `$(lsb_release -cs)` automatiquement par ton code Ubuntu (ex: `jammy`, `focal`, etc.)

```bash
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

---

## 🔄 5️⃣ Mets à jour les paquets

```bash
sudo apt update
```

⚠️ Ici, tu devrais maintenant voir une ligne comme :

```
Get: https://download.docker.com/linux/ubuntu jammy InRelease [48.9 kB]
```

Si tu vois ça → c’est bon signe ✅

---

## 🐋 6️⃣ Installe Docker et Compose (nouvelle méthode officielle)

```bash
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

---

## 🧪 7️⃣ Vérifie les versions installées

```bash
docker --version
docker compose version
```

Tu devrais obtenir :

```
Docker version 27.x.x, build ...
Docker Compose version v2.x.x
```

---

## ⚙️ 8️⃣ Active Docker au démarrage

```bash
sudo systemctl enable docker
sudo systemctl start docker
sudo systemctl status docker
```

---

## 👤 9️⃣ Permet d’utiliser Docker sans sudo

```bash
sudo usermod -aG docker $USER
```

Puis **reconnecte-toi** à ton EC2 (pour que le changement soit pris en compte) :

```bash
exit
```

Puis reconnecte-toi.

---

## ✅ 10️⃣ Test final

```bash
docker run hello-world
docker compose version
```

➡️ Si ça fonctionne, Docker est correctement installé 🎉

---

# ⚡ Alternative (si tu veux aller plus vite)

Si jamais le dépôt Docker est encore inaccessible pour ta version d’Ubuntu, tu peux installer **la version officielle via script** :

```bash
curl -fsSL https://get.docker.com | sudo bash
```

Puis :

```bash
sudo usermod -aG docker $USER
newgrp docker
docker --version
docker compose version
```

