
# **AWS Messaging : Spring Boot avec LocalStack**

Ce projet d’application Spring Boot montre comment :

* Déployer une infrastructure CloudFormation sur LocalStack
* Configurer des abonnements SNS → SQS via CloudFormation
* Recevoir des messages SQS avec le SDK Java AWS
* Envoyer des emails avec AWS SES via le SDK Java AWS

---

# ✅ **Prérequis**

* **Java 11+**
* **Maven 3+**
* **LocalStack** (simulateur local des services AWS)
* **awslocal** (wrapper AWS CLI pour LocalStack)

---

# 🚀 **Comment exécuter le projet**

## 1️⃣ **Prérequis**

* **Java 11+**
* **Maven 3+**
* **LocalStack** (simulateur local des services AWS)
* **awslocal** (wrapper AWS CLI pour LocalStack) 

## 1️⃣ **Construire l’application**

Il s’agit d’une application Spring Boot classique, compilée avec :

```bash
mvn clean install
```

---

## 2️⃣ **Lancer l’infrastructure sur LocalStack**

L’infrastructure est définie dans le fichier CloudFormation :

```
src/main/resources/email-infra.yml
```

### ➤ Démarrer LocalStack + le serveur SMTP
```bash
LOCALSTACK_AUTH_TOKEN=<your-api-key> docker-compose up -d
```

### ➤ Déployer la stack CloudFormation

```bash
awslocal cloudformation deploy \
    --template-file src/main/resources/email-infra.yml \
    --stack-name email-infra
```

---

## 3️⃣ **Démarrer l’application Spring Boot**

Vous devez définir deux variables d’environnement :

```bash
AWS_ACCESS_KEY_ID=test AWS_SECRET_ACCESS_KEY=test mvn spring-boot:run
```

(Ces valeurs sont fictives car LocalStack n’a pas besoin de vraies clés.)

---

## 4️⃣ **Tester l’application**

### ✔ Vérifier l’email expéditeur

```bash
awslocal ses verify-email-identity --email-address no-reply@localstack.cloud
```

### verify 
```bash 
awslocal ses list-identities
```

### ✔ Envoyer un message SNS

```bash
awslocal sns publish \
    --topic arn:aws:sns:us-east-1:000000000000:email-notifications \
    --message '{"subject":"hello", "address": "alice@example.com", "body": "hello world"}'
```

### ✔ Vérifier les messages dans la file SQS via l’endpoint `/list`

```bash
curl -s localhost:8080/list | jq .
```

### ✔ Traiter les messages et envoyer les emails

```bash
curl -s localhost:8080/process
```

### ✔ Vérifier les emails envoyés

👉 Via MailHog : [http://localhost:8025/](http://localhost:8025/)
👉 Via l’endpoint interne SES de LocalStack :

```bash
curl -s localhost:4566/_localstack/ses | jq .
```

---

# 🧠 **Explication détaillée des services AWS et de leurs rôles**


# 🟦 **1. AWS CloudFormation — Déploiement automatique de l’infrastructure**

CloudFormation permet de **définir et déployer l'architecture AWS sous forme de code (IaC)**.

Dans ce projet, CloudFormation crée automatiquement :

* un **topic SNS**
* une **file SQS**
* un **abonnement SNS → SQS**
* les politiques d’accès nécessaires

**Rôle :**
➡ Automatiser toute l’infrastructure sans cliquer dans AWS.
➡ Résultat : déploiement reproductible, versionné et contrôlé.

---

# 🟧 **2. AWS SNS (Simple Notification Service) — Service de publication/subscription**

SNS est un service de **messagerie pub/sub**.

Dans ce projet :

* l’application (ou un service externe) **publie un message dans le topic SNS**
* SNS redirige le message vers la file SQS qui y est abonnée

**Rôle :**
➡ Servir de **point d’entrée** des notifications.
➡ Distribuer les messages à un ou plusieurs abonnés.

---

# 🟩 **3. AWS SQS (Simple Queue Service) — File de messages**

SQS est une file utilisée pour :

* découpler les systèmes
* absorber une grande charge de messages
* garantir la livraison même si les services consommateurs sont offline

Dans ce projet :

* SQS reçoit les messages envoyés depuis le topic SNS
* L’application Spring Boot **lit SQS grâce au SDK AWS**
* Chaque message contient :

  * un sujet
  * une adresse email du destinataire
  * un contenu

**Rôle :**
➡ Assurer une messagerie fiable entre SNS et Spring Boot.

---

# 🟪 **4. AWS SES (Simple Email Service) — Envoi d’emails**

SES est un service pour envoyer des emails transactionnels.

Dans ce projet :

* Après avoir lu les messages dans SQS
* L’application Spring Boot utilise **AWS SES** pour envoyer un email au destinataire
* L'email est simulé par LocalStack (et visualisable via MailHog)

**Rôle :**
➡ Convertir un message métier en un **email réel** envoyé à l’utilisateur final.

---

# 🟫 **5. LocalStack — Simulateur AWS sur votre machine**

LocalStack émule de nombreux services AWS :

* SNS
* SQS
* SES
* CloudFormation
* Lambda
* etc.

Sans coût AWS, sans connexion Internet.

**Rôle :**
➡ Permettre un développement 100 % local
➡ Tester une architecture AWS complète sans payer


