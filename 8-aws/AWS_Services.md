## Vue d’ensemble des principaux services AWS

Voici une présentation structurée des familles de services AWS + les services majeurs + ce que ça fait + comment se structure leur tarification (“coût professionnel”).

---

## 1. Compute (Calcul)

Les services de calcul permettent d’exécuter des applications, des serveurs, des conteneurs, des fonctions sans server, etc.

| Service                                | Description                                                                                                                                                     | Modèle de coût                                                                                                                                                                                                                             |
| -------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Amazon EC2 (Elastic Compute Cloud)** | Ce sont des machines virtuelles dans le cloud : tu peux lancer des “instances” (serveurs) avec différents types (CPU, RAM, GPU, etc.). ([AWS Documentation][1]) | Tarification à la seconde (minimum 60 s pour certaines instances). On-Demand (pay-as-you-go), Reserved Instances (engagement 1 ou 3 ans), Spot (instances “à rabais” utilisant la capacité non utilisée). ([Amazon Web Services, Inc.][2]) |
| **AWS Lambda**                         | Exécution de code sans gérer de serveur (“serverless”) : tu upload ton code, tu déclenches des fonctions à la demande.                                          | Pay-per-invocation + durée d’exécution : tu paies en fonction du nombre de requêtes + du temps d’exécution du code.                                                                                                                        |
| **AWS Fargate**                        | Service de calcul pour les conteneurs : tu exécutes des conteneurs Docker sans gérer les instances EC2 sous-jacentes.                                           | Tu paies pour la vCPU et la mémoire que les tâches Fargate utilisent, à l’heure (ou fraction).                                                                                                                                             |
| **Elastic Beanstalk**                  | Service pour déployer des applications web (Java, .NET, Node.js, etc.) facilement : AWS gère le provisionnement, le scaling, le load balancing.                 | Tu paies pour les ressources sous-jacentes (EC2, RDS, etc.), Beanstalk lui-même n’a pas de coût additionnel, mais dépend des autres services.                                                                                              |

---

## 2. Storage (Stockage)

Stocker des données (objets, blocs, fichiers) de façon scalable et sécurisée.

| Service                                | Description                                                                                                   | Modèle de coût                                                                                              |
| -------------------------------------- | ------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| **Amazon S3 (Simple Storage Service)** | Stockage d’objets (fichiers, images, sauvegardes, data lakes, etc.). Très scalable, durable. ([Wikipedia][3]) | Tu paies en fonction du volume stocké (par Go), des requêtes (GET, PUT…) et du data transfer.               |
| **Amazon EBS (Elastic Block Store)**   | Stockage de blocs persistant, attaché aux instances EC2 comme des disques durs virtuels.                      | Tarification selon la capacité provisionnée (Go) + type d’IO (par exemple, provisioned IOPS).               |
| **Amazon EFS (Elastic File System)**   | Système de fichiers partagé (file system) accessible par plusieurs instances EC2.                             | Paye selon l’espace de stockage utilisé, parfois selon les performances (standard vs “infrequent access”).  |
| **Amazon S3 Glacier (Glacier)**        | Stockage d’archives à long terme, peu coûteux, mais avec des latences de restauration plus élevées.           | Très faible coût de stockage, mais des frais pour “restauration” des données (quand tu veux les récupérer). |

---

## 3. Base de données (Database)

Services pour des bases de données relationnelles, NoSQL, en mémoire, graphes, etc.

| Service                                      | Description                                                                                             | Cas d’usage / avantages                                                                                                 |
| -------------------------------------------- | ------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| **Amazon RDS (Relational Database Service)** | Base relationnelle gérée (MySQL, PostgreSQL, Oracle, SQL Server, Aurora, etc.). ([Wikipedia][4])        | Simplifie la gestion : mises à jour, sauvegardes, scaling, réplication. Très utilisé pour des applis transactionnelles. |
| **Amazon DynamoDB**                          | Base NoSQL (clé-valeur / document) gérée, très haute performance, “serverless” au niveau de la gestion. | Idéale pour des applis à faible latence, grand volume de requêtes, scale horizontal.                                    |
| **Amazon ElastiCache**                       | Cache en mémoire : Redis ou Memcached géré. ([Wikipedia][5])                                            | Améliore la performance d’applications en stockant des données fréquemment consultées en mémoire.                       |
| **Amazon Neptune**                           | Base de données graphe. Supporte Gremlin, SPARQL, etc. ([Wikipedia][6])                                 | Très utile pour des données fortement connectées : réseaux sociaux, recommandations, graphes de connaissances.          |
| **Amazon Redshift**                          | Entrepôt de données (data warehouse) pour l'analytique à grande échelle.                                | Pour analyser de grandes quantités de données, faire des requêtes complexes, des agrégations, des rapports BI.          |

---

## 4. Analytics

Services pour traitement de données, flux (stream), data lakes, ETL, BI.

Quelques exemples :

* **Amazon Kinesis** : permet de traiter en temps réel des flux de données (streaming). ([Wikipedia][7])
* **AWS Glue** : service d’ETL (Extract, Transform, Load), très utile pour préparer des données pour l’analyse.
* **Amazon EMR (Elastic MapReduce)** : cluster Hadoop / Spark managé pour du big data.
* **Amazon Athena** : permet de faire des requêtes SQL directement sur des fichiers stockés dans S3, sans avoir à déplacer les données.

---

## 5. Machine Learning / IA

AWS propose des services gérés pour le machine learning, l’IA, le traitement de la voix, du texte, des images, etc.

Quelques exemples :

* **Amazon SageMaker** : plateforme pour créer, entraîner et déployer des modèles ML. ([Wikipedia][8])
* **Amazon Rekognition** : reconnaissance d’images / vidéos (visage, objets, étiquettes).
* **Amazon Lex** : pour créer des chatbots (NLU, NLP).
* **Amazon Polly** : service de synthèse vocale (“text-to-speech”).
* **Amazon Translate**, **Transcribe**, **Comprehend** : traduction, transcription, compréhension de texte.
* **Amazon Q** : (selon la version) IA générative / agentique, dépend des offres actuelles.

---

## 6. Réseau & Content Delivery (Mise en réseau / CDN)

Services pour organiser le réseau, distribuer du contenu, sécuriser les accès, etc.

* **Amazon VPC (Virtual Private Cloud)** : te permet de créer un réseau virtuel isolé dans AWS. Très utile pour la sécurité, le contrôle des sous-réseaux, des routeurs, des accès.
* **Amazon Route 53** : service DNS + gestion de domaine + routage intelligent.
* **Amazon CloudFront** : CDN (Content Delivery Network), pour distribuer du contenu très rapidement à des utilisateurs partout dans le monde. Coût dépend du trafic, des requêtes HTTP/HTTPS, etc. ([Amazon Web Services, Inc.][9])
* **Elastic Load Balancing (ELB)** : répartit le trafic réseau entre plusieurs instances EC2 ou autres ressources.

---

## 7. Sécurité, Identité et Conformité (Security, Identity & Compliance)

Services qui aident à sécuriser les ressources, contrôler l’accès, gérer des clés, etc.

* **AWS IAM (Identity and Access Management)** : permet de gérer les utilisateurs, les rôles, les politiques d’accès. Très central pour la sécurité. ([AWS Documentation][10])
* **AWS KMS (Key Management Service)** : gestion des clés de chiffrement pour protéger les données.
* **AWS Secrets Manager** : stockage sécurisé des secrets (mots de passe, tokens).
* **AWS CloudTrail** : journalisation des appels API pour audit et sécurité.
* **AWS Shield / WAF** : protection contre les attaques DDoS / pare-feu web.

---

## 8. Gestion & Gouvernance (Management & Governance)

Services pour monitorer, automatiser, configurer, diagnostiquer :

* **Amazon CloudWatch** : surveillance des métriques (CPU, mémoire, logs, alertes).
* **AWS Config** : suivre l’inventaire des ressources, leurs configurations, et voir les modifications.
* **AWS Systems Manager** : gérer les instances EC2, appliquer des patchs, exécuter des commandes, etc.
* **AWS Organizations** : structurer plusieurs comptes AWS, appliquer des politiques (SCP), consolider la facturation.
* **AWS Trusted Advisor** : recommandations sur les bonnes pratiques (sécurité, coût, performance).

---

## 9. Migration & Transfert

Services pour migrer des données, des serveurs, des bases de données vers AWS :

* **AWS Database Migration Service (DMS)** : migrer des bases de données vers AWS avec peu de downtime.
* **AWS Application Migration Service** : migrer des applications on-prem vers AWS.
* **AWS Snow Family** (Snowball, Snowmobile) : pour transporter de très gros volumes de données physiquement (lorsque la bande passante n’est pas suffisante / trop coûteuse).

---

## 10. Coût & Finance (Cloud Financial Management)

Des outils spécifiques pour gérer les coûts, budgets, et optimiser :

* **AWS Cost Explorer** : permet d’analyser tes dépenses AWS, quels services coûtent le plus, visualiser l’évolution.
* **AWS Budgets** : créer des budgets (mensuels, trimestriels) et être alerté quand tu dépasses des seuils.
* **Savings Plans** : engagement de consommation (en $/heure) pour obtenir des réductions (utilisé notamment pour EC2, Fargate, etc.). ([Amazon Web Services, Inc.][11])

---

## Exemple de structure de **coût professionnel** AWS

Quand on parle de “coût professionnel” sur AWS, cela implique souvent :

1. **Utilisation “on-demand”** : tu payes ce que tu consommes, sans engagement. Cela coûte plus cher par unité, mais tu restes très flexible.
2. **Engagements (Reserved Instances, Savings Plans)** : si tu es certain de l’usage (ex : un serveur qui tourne 24/7), tu prends un engagement 1 ou 3 ans, ce qui réduit fortement le coût.
3. **Utilisation Spot** : tu utilises des capacités non utilisées à prix très réduit, mais ces instances peuvent être interrompues.
4. **Coûts additionnels** : ce n’est pas juste le calcul / CPU — il faut aussi prendre en compte :

   * le stockage (S3, EBS, etc.)
   * le transfert de données (data out, entre services)
   * les requêtes API (dans certains services)
   * la mise en cache / CDN
   * la surveillance / logging
   * la sécurisation (KMS, IAM)
5. **Optimisation** : très souvent, des grosses économies se font en optimisant l’architecture (ex : faire du right-sizing EC2, nettoyer les volumes EBS non utilisés, utiliser CloudFront pour réduire le coût de transfert S3).

---

[1]: https://docs.aws.amazon.com/whitepapers/latest/aws-overview/compute-services.html?utm_source=chatgpt.com "AWS Compute Services category iconCompute - Overview of Amazon Web Services"
[2]: https://aws.amazon.com/ec2/pricing/on-demand/?utm_source=chatgpt.com "EC2 On-Demand Instance Pricing"
[3]: https://en.wikipedia.org/wiki/Amazon_S3?utm_source=chatgpt.com "Amazon S3"
[4]: https://en.wikipedia.org/wiki/Amazon_Relational_Database_Service?utm_source=chatgpt.com "Amazon Relational Database Service"
[5]: https://en.wikipedia.org/wiki/Amazon_ElastiCache?utm_source=chatgpt.com "Amazon ElastiCache"
[6]: https://en.wikipedia.org/wiki/Amazon_Neptune?utm_source=chatgpt.com "Amazon Neptune"
[7]: https://en.wikipedia.org/wiki/Amazon_Kinesis?utm_source=chatgpt.com "Amazon Kinesis"
[8]: https://en.wikipedia.org/wiki/Amazon_SageMaker?utm_source=chatgpt.com "Amazon SageMaker"
[9]: https://aws.amazon.com/cloudfront/pricing/?utm_source=chatgpt.com "Amazon CloudFront CDN - Plans & Pricing - Try For Free"
[10]: https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html?utm_source=chatgpt.com "What is IAM? - AWS Identity and Access Management"
[11]: https://aws.amazon.com/ec2/pricing/?utm_source=chatgpt.com "Amazon EC2 – Secure and resizable compute capacity – AWS"
