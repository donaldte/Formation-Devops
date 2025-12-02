# 🚀 INSTALLER AWS LOCALSTACK

## Prérequis

- Docker
- Docker Compose



# ✅ **1. Créer une VM ou utiliser votre machine**

## 🔧 **Configuration recommandée**

Pour LocalStack + Docker + Terraform :

* **2 vCPU**
* **4 GB RAM**
* **80 GB SSD**
* **Ubuntu 22.04 LTS**

# 🟢 **2. Se connecter à la machine**

Depuis PowerShell dans ton Windows :

```bash
ssh root@YOUR_SERVER_IP
```


# ✔️ **3. Installer Docker sur ton serveur DigitalOcean**

Commande officielle :

```bash
apt update -y
apt install -y ca-certificates curl gnupg lsb-release
```

Ajouter le dépôt Docker :

```bash
mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
```

```bash
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" > /etc/apt/sources.list.d/docker.list
```

Installer Docker Engine :

```bash
apt update -y
apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
```

Lancer et activer Docker :

```bash
systemctl start docker
systemctl enable docker
```

Tester Docker :

```bash
docker run hello-world
```

---

# 🟢 **4. Installer LocalStack**

Installer pip :

```bash
apt install -y python3-venv python3-pip
```

Créer un environnement virtuel :

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Installer LocalStack Community :

```bash
python3 -m pip install --upgrade localstack
```

Installer LocalStack Pro :

```bash
python3 -m pip install "localstack[pro]"
```

Installer AWS CLI :

```bash
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

---

# 🚀 **5. Lancer LocalStack**

```bash
localstack start -d
```

Vérifier qu’il tourne :

```bash
docker ps
```

Tu verras :

```
localstack/localstack
```

---

# 🟢 **6. Configurer AWS CLI (côté serveur ou côté Windows)**

Dans ta machine :

```bash
aws configure
```

Valeurs à mettre :

```
AWS Access Key ID: test
AWS Secret Access Key: test
Default region name: us-east-1
```

Tester une commande S3 :

```bash
aws --endpoint-url=http://localhost:4566 s3 mb s3://mybucket
aws --endpoint-url=http://localhost:4566 s3 ls
```

Si ça marche → **LocalStack est opérationnel !**

---

# 🧩 **7. Connecter ton Windows à LocalStack sur DigitalOcean**

Depuis ton PC :

```bash
aws --endpoint-url=http://YOUR_IP:4566 s3 ls
```

→ Et tu verras les buckets créés sur le serveur DigitalOcean.

C’est 100% fonctionnel pour tous tes labs.

---

# 🧪 **8. Prochaines étapes : projets DevOps**

Une fois ton environnement prêt, tu peux pratiquer :

### ✔ Pipeline CI/CD CodePipeline + CodeBuild + CodeDeploy

### ✔ API Gateway + Lambda + DynamoDB

### ✔ ECS Fargate + ALB

### ✔ Monitoring (CloudWatch)

### ✔ Terraform + LocalStack

### ✔ IAM + KMS + Secrets Manager

### ✔ SQS + SNS + Lambda Event-driven

