
## **AWS EKS – Introduction**

### **Table des matières** :

### Comprendre les fondamentaux de Kubernetes

**1.1 EKS vs Kubernetes auto-géré : Avantages et inconvénients**

### Configuration de votre environnement AWS pour EKS

**2.1 Création d’un compte AWS et configuration des utilisateurs IAM**
**2.2 Configuration de l’AWS CLI et de kubectl**
**2.3 Préparation du réseau et des groupes de sécurité pour EKS**

### Lancer votre premier cluster EKS

**3.1 Utilisation de la console EKS pour créer un cluster**
**3.2 Création d’un cluster EKS via l’AWS CLI**
**3.3 Authentification avec le cluster EKS**

### Déploiement d'applications sur EKS

**4.1 Conteneurisation des applications avec Docker**
**4.2 Écriture des fichiers YAML de déploiement Kubernetes**
**4.3 Déploiement d’applications sur EKS : Guide étape par étape**

---

## **Comprendre les fondamentaux de Kubernetes**

### **1.1 EKS vs Kubernetes auto-géré : Avantages et inconvénients**

#### **1.1.1 Avantages d’EKS (Amazon Elastic Kubernetes Service)** :

* **Plan de contrôle géré** : EKS prend en charge la gestion des composants du plan de contrôle Kubernetes, comme le serveur API, le contrôleur principal et etcd. AWS s’occupe des mises à jour, des correctifs et assure la haute disponibilité.

* **Mises à jour automatiques** : EKS met automatiquement à jour la version de Kubernetes, éliminant les interventions manuelles et assurant l’accès aux dernières fonctionnalités et correctifs de sécurité.

* **Scalabilité** : Le plan de contrôle peut s’adapter automatiquement à la charge, garantissant la réactivité du cluster.

* **Intégration avec AWS** : EKS s’intègre naturellement aux services AWS (IAM pour l’authentification, VPC pour le réseau, équilibreurs de charge pour exposer les services, etc.).

* **Sécurité et conformité** : EKS est conçu pour respecter de nombreuses normes de sécurité et exigences réglementaires.

* **Surveillance et journalisation** : Intégration avec **CloudWatch** pour surveiller la santé du cluster et les métriques de performance.

* **Écosystème actif** : En tant que service managé, EKS bénéficie de contributions continues de la communauté Kubernetes.

#### **Inconvénients** :

* **Coût** : Étant un service managé, EKS peut coûter plus cher que Kubernetes auto-géré, surtout pour les grands déploiements.

* **Moins de contrôle** : Moins de flexibilité sur la configuration et l'infrastructure sous-jacente.

---

#### **1.1.2 Avantages de Kubernetes auto-géré sur EC2** :

* **Économie de coûts** : Possibilité d’utiliser des instances EC2 à prix réduit (spot ou réservées).

* **Flexibilité** : Contrôle total sur la configuration et l’optimisation du cluster selon les besoins.

* **Compatibilité AWS** : Peut utiliser d'autres services AWS tout en restant auto-géré.

* **Fonctionnalités expérimentales** : Possibilité de tester les dernières versions de Kubernetes non encore prises en charge par EKS.

#### **Inconvénients** :

* **Complexité** : Mise en place et gestion plus compliquées, surtout pour les débutants.

* **Maintenance manuelle** : Les mises à jour, correctifs, et haute disponibilité doivent être gérés manuellement.

* **Scalabilité difficile** : L’évolution du plan de contrôle demande une planification rigoureuse.

* **Sécurité** : Plus d’efforts nécessaires pour atteindre les standards de sécurité.

* **Moins d’automatisation** : Plus de scripts et d’actions manuelles nécessaires, augmentant les risques d’erreur.

---

## **Configurer votre environnement AWS pour EKS**

### **2.1 Création d’un compte AWS et configuration des utilisateurs IAM**

**Créer un compte AWS** :

* Rendez-vous sur [https://aws.amazon.com/](https://aws.amazon.com/) et cliquez sur **« Créer un compte AWS »**.
* Fournissez votre adresse e-mail, mot de passe et informations de facturation.

**Accéder à la console AWS** :

* Suivez le lien de vérification envoyé par e-mail pour activer votre compte.

**Configurer l’authentification multifactorielle (MFA)** (recommandé) :

* Une fois connecté à la console, activez la MFA pour plus de sécurité.

**Créer des utilisateurs IAM** :

* Allez dans le service IAM > « Utilisateurs » > « Ajouter un utilisateur ».
* Définissez les types d'accès (console AWS, accès programmatique, ou les deux).
* Attribuez des groupes ou des politiques d’accès.

**Accès programmatique** :

* Des clés d’accès (ID et secret) vous seront fournies. Conservez-les en lieu sûr.

---

### **2.2 Configuration de l’AWS CLI et de kubectl**

**Installation de l’AWS CLI** :

* Téléchargez et installez l’AWS CLI selon votre OS.

**Configurer l’AWS CLI** :

```bash
aws configure
```

* Fournissez la clé d’accès, la région par défaut et le format de sortie.

**Installer kubectl** :

* Installez `kubectl` selon les instructions officielles.

**Configurer kubectl pour EKS** :

```bash
aws eks update-kubeconfig --name nom-de-votre-cluster
```

* Vérifiez la connexion :

```bash
kubectl get nodes
```

---

### **2.3 Préparation du réseau et des groupes de sécurité pour EKS**

#### **Créer un VPC (Virtual Private Cloud)** :

* Allez dans **VPC** > « Créer un VPC ».
* Définissez le CIDR IPv4, les sous-réseaux publics/privés et les zones de disponibilité.

---

#### **Configurer les groupes de sécurité** :

* Les groupes de sécurité jouent le rôle de pare-feu virtuel.
* Allez dans **VPC > Groupes de sécurité > Créer**.
* Définissez les **règles entrantes** (ex : SSH, trafic interne) et **règles sortantes** (ex : vers Internet ou AWS).

**Associer le groupe de sécurité** :

* Lors du lancement des nœuds EKS, utilisez l’ID du groupe de sécurité défini.

---

#### **Configurer une passerelle Internet (Internet Gateway)** :

* Allez dans **VPC > Passerelles Internet > Créer**.
* Attachez la passerelle à votre VPC.
* Modifiez les **tables de routage** pour acheminer le trafic externe via la passerelle (route `0.0.0.0/0` vers l’IGW).

---

#### **Configurer les politiques IAM** :

* Allez dans **IAM > Politiques > Créer**.
* Rédigez votre politique en JSON (ex : autorisations EC2, ECR, ELB, etc.).

**Attacher la politique à un rôle IAM** :

* Allez dans **IAM > Rôles > Sélectionner le rôle** > « Joindre une politique ».
* Associez le rôle IAM aux nœuds EKS.

**Mise à jour de la configuration des nœuds EKS** :

* Lors du lancement, spécifiez l’ARN du rôle IAM pour les nœuds.

---

En complétant ces étapes, votre environnement AWS est prêt à accueillir un cluster EKS. Vous pouvez maintenant le créer via la **console AWS** ou la **CLI**, comme décrit dans la section 3.

