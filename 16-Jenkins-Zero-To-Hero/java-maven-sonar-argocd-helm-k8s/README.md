

# 🚀 Pipeline Jenkins pour une application Java avec Maven, SonarQube, Argo CD, Helm et Kubernetes

# image de jenkins pipeline


## ✅ **Prérequis**

* Code de l’application Java hébergé sur un dépôt Git
* Serveur Jenkins opérationnel
* Cluster Kubernetes fonctionnel
* Gestionnaire de paquets Helm installé
* Argo CD installé pour la partie CD

---

## 🧩 **Étapes de mise en place**

---

## **1. Installer les plugins nécessaires dans Jenkins**

1.1 **Git plugin** → Nom dans la liste : `Git`
1.2 **Maven Integration plugin** → Nom dans la liste : `Maven Integration`
1.3 **Docker Pipeline plugin** → Nom dans la liste : `Docker Pipeline`
1.4 **Kubernetes Continuous Deploy plugin** → Nom dans la liste : `Kubernetes Continuous Deploy`

---

## **2. Créer un nouveau pipeline Jenkins**

2.1 Dans Jenkins, crée un nouveau job *Pipeline* et configure-le avec l’URL du dépôt Git contenant l’application Java.
2.2 Ajoute un **Jenkinsfile** à ton dépôt Git pour définir les différentes étapes du pipeline.

---

## **3. Définir les étapes du pipeline**

Voici un pipeline CI/CD complet et classique :

* **Stage 1 : Checkout** → Récupérer le code source depuis Git
* **Stage 2 : Build** → Compiler l’application avec Maven
* **Stage 3 : Tests unitaires** → Exécuter JUnit / Mockito
* **Stage 4 : Analyse SonarQube** → Vérifier la qualité du code
* **Stage 5 : Packaging** → Générer le JAR
* **Stage 6 : Déploiement de test avec Helm**
* **Stage 7 : Tests d’acceptation utilisateur (UAT)**
* **Stage 8 : Promotion en production via Argo CD**

---

## **4. Configurer chaque étape dans Jenkins**

### **Stage 1 – Checkout**

Utilise le plugin **Git** pour cloner le dépôt.

### **Stage 2 – Build Maven**

Utilise le plugin **Maven Integration** pour compiler.

### **Stage 3 – Tests unitaires**

Utilise JUnit / Mockito pour exécuter les tests.

### **Stage 4 – Analyse SonarQube**

Utilise le plugin **SonarQube Scanner** pour analyser la qualité du code.

### **Stage 5 – Package**

Utilise Maven pour créer le fichier `.jar`.

### **Stage 6 – Déploiement de test avec Helm**

Utilise le plugin **Kubernetes Continuous Deploy** pour appliquer le chart Helm.

### **Stage 7 – Tests d'acceptation**

Exécute des tests automatiques (ex. Selenium, Cypress, Robot Framework).

### **Stage 8 – Déploiement en production (CD)**

Utilise **Argo CD** pour synchroniser avec les manifests Git et déployer.

---

## **5. Configuration d’Argo CD**

* Installer Argo CD sur ton cluster Kubernetes
* Créer un dépôt Git *GitOps* que Argo CD suivra
* Créer un **Helm chart** pour ton application Java
* Pousser ce chart dans le dépôt Git suivi par Argo CD

---

## **6. Intégration Jenkins → Argo CD**

6.1 Ajouter un token API Argo CD dans les *Credentials* Jenkins
6.2 Ajouter une étape spécifique dans ton Jenkinsfile pour déclencher la synchronisation Argo CD (ou laisser Argo CD en mode auto-sync)

---

## **7. Lancer le pipeline Jenkins**

7.1 Déclencher le pipeline (manuellement ou via webhook Git)
7.2 Suivre l’exécution des différentes étapes
7.3 Corriger toute erreur détectée pendant le build, les tests ou l’analyse SonarQube

---

## 🎯 **Conclusion**

Ce pipeline CI/CD complet :

* Automatise le build Java
* Vérifie la qualité du code avec SonarQube
* Exécute les tests
* Construit et package l’application
* Déploie sur Kubernetes via Helm
* Promeut en production via Argo CD
* Fournit un processus robuste, moderne et totalement automatisé