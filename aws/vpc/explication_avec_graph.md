# Cours Complet et Détaillé sur les VPC AWS avec Diagrammes

## Table des Matières
1. [Introduction aux VPC](#1-introduction-aux-vpc)
2. [Concepts Fondamentaux de Réseau](#2-concepts-fondamentaux-de-réseau)
3. [Composants Détaillés du VPC](#3-composants-détails-du-vpc)
4. [Architectures Avancées](#4-architectures-avancées)
5. [Sécurité et Bonnes Pratiques](#5-sécurité-et-bonnes-pratiques)
6. [Monitoring et Troubleshooting](#6-monitoring-et-troubleshooting)

---
## 1. Introduction aux VPC

### 1.1. Définition d'un VPC

**VPC (Virtual Private Cloud)** : C'est un réseau virtuel isolé et sécurisé dans le cloud AWS où vous pouvez déployer vos ressources informatiques.

```
┌─────────────────────────────────────────┐
│                VPC AWS                  │
│  ┌─────────────┐  ┌─────────────┐      │
│  │  Subnet A   │  │  Subnet B   │      │
│  │ ┌─────────┐ │  │ ┌─────────┐ │      │
│  │ │ EC2     │ │  │ │ RDS     │ │      │
│  │ │ Instance│ │  │ │ Database│ │      │
│  │ └─────────┘ │  │ └─────────┘ │      │
│  └─────────────┘  └─────────────┘      │
│          │                   │         │
│    ┌─────┴───────┐    ┌──────┴─────┐   │
│    │ Route Table │    │ Security   │   │
│    │             │    │  Group     │   │
│    └─────────────┘    └────────────┘   │
└─────────────────────────────────────────┘
```

### 1.2. Architecture de Base d'un VPC

```
┌─────────────────────────────────────────────────────────────┐
│                         VPC (10.0.0.0/16)                   │
├─────────────────┬─────────────────┬─────────────────────────┤
│   Subnet Public │  Subnet Privé   │   Subnet Isolé         │
│   (10.0.1.0/24) │  (10.0.2.0/24)  │   (10.0.3.0/24)        │
│                 │                 │                        │
│  ┌────────────┐ │  ┌────────────┐ │  ┌────────────┐        │
│  │   EC2      │ │  │   EC2      │ │  │  RDS       │        │
│  │  Web       │ │  │   App      │ │  │ Database   │        │
│  │ Server     │ │  │  Server    │ │  │            │        │
│  └────────────┘ │  └────────────┘ │  └────────────┘        │
│        │        │        │        │         │              │
│  ┌─────┴─────┐  │  ┌─────┴─────┐  │  ┌─────┴─────┐         │
│  │  IGW      │  │  │ NAT       │  │  │  Aucune   │         │
│  │ Route     │  │  │ Gateway   │  │  │  Route    │         │
│  │ 0.0.0.0/0│  │  │  Route    │  │  │  Internet │         │
│  └───────────┘  │  └───────────┘  │  └───────────┘         │
└─────────────────┴─────────────────┴─────────────────────────┘
```

---

## 2. Concepts Fondamentaux de Réseau

### 2.1. Adressage IP et CIDR - Visualisation

#### Notation CIDR et Masques
```
CIDR    | Masque         | Adresses | Exemple de Plage
--------|----------------|----------|-------------------
/16     | 255.255.0.0    | 65,536   | 10.0.0.0 - 10.0.255.255
/20     | 255.255.240.0  | 4,096    | 10.0.0.0 - 10.0.15.255
/24     | 255.255.255.0  | 256      | 10.0.1.0 - 10.0.1.255
/28     | 255.255.255.240| 16       | 10.0.1.0 - 10.0.1.15
```

#### Structure d'une Adresse IP
```
Adresse IP: 192.168.1.150
Binaire:    11000000.10101000.00000001.10010110

Masque:     /24 (255.255.255.0)
Binaire:    11111111.11111111.11111111.00000000

Réseau:     192.168.1.0/24
Plage:      192.168.1.1 - 192.168.1.254
Broadcast:  192.168.1.255
```

### 2.2. Plan d'Adressage VPC - Exemple Complet

```
VPC Principal: 10.0.0.0/16 (65,536 adresses)

┌─────────────────────────────────────────────────────────────────┐
│                         10.0.0.0/16                            │
├─────────────────┬─────────────────┬─────────────────┬───────────┤
│   Web Tier      │   App Tier      │  Data Tier      │ Réservé  │
│   10.0.0.0/19   │  10.0.32.0/19   │ 10.0.64.0/19    │10.0.96.0/19│
│   (8,192 IPs)   │  (8,192 IPs)    │ (8,192 IPs)     │(8,192 IPs)│
├─────────────────┼─────────────────┼─────────────────┼───────────┤
│ AZ A: 10.0.1.0/24│ AZ A: 10.0.33.0/24│ AZ A: 10.0.65.0/24│         │
│ AZ B: 10.0.2.0/24│ AZ B: 10.0.34.0/24│ AZ B: 10.0.66.0/24│         │
│ AZ C: 10.0.3.0/24│ AZ C: 10.0.35.0/24│ AZ C: 10.0.67.0/24│         │
└─────────────────┴─────────────────┴─────────────────┴───────────┘
```

### 2.3. Sous-réseau AWS - Adresses Réservées

```
Sous-réseau: 10.0.1.0/24 (256 adresses)

┌─────────────────────────────────────────────────────────┐
│                   10.0.1.0/24                          │
├─────────────┬─────────────┬─────────────┬─────────────┤
│  Réseau     │   Routeur   │    DNS      │ Réservé    │ Broadcast │
│   10.0.1.0  │  10.0.1.1   │  10.0.1.2   │ 10.0.1.3   │ 10.0.1.255│
├─────────────┼─────────────┼─────────────┼─────────────┼───────────┤
│   Première  │            Adresses Utilisables          │ Dernière │
│  Adresse    │         (10.0.1.4 - 10.0.1.254)          │ Adresse  │
│  10.0.1.4   │                                           │ 10.0.1.254│
└─────────────┴───────────────────────────────────────────┴───────────┘
```

---

## 3. Composants Détaillés du VPC

### 3.1. Internet Gateway (IGW) - Flux de Données

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Internet      │    │  Internet        │    │   VPC           │
│                 │    │   Gateway        │    │   10.0.0.0/16   │
│    Public       │◄──►│   (IGW)          │◄──►│                 │
│    Internet     │    │                  │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                        │                       │
         │                        │              ┌────────┴────────┐
         │                        │         ┌─────┴─────┐    ┌─────┴─────┐
         │                        │         │ Subnet    │    │ Subnet    │
         │                        │         │ Public    │    │ Privé     │
         │                        │         │ 10.0.1.0/24│    │10.0.2.0/24│
         └────────────────────────┼─────────┼───────────┘    └───────────┘
                                  │         │                      │
                                  │         └──────┬────────┬──────┘
                                  │                │        │
                                  │          ┌─────┴────┐ ┌─┴─────┐
                                  │          │  EC2     │ │  EC2   │
                                  │          │ avec IP  │ │ sans IP│
                                  │          │ Publique │ │ Publique│
                                  │          └──────────┘ └────────┘
                                  │
                                  └─────► Route: 0.0.0.0/0 → igw-xxxx
```

### 3.2. NAT Gateway - Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                          VPC 10.0.0.0/16                       │
├─────────────────────────────┬───────────────────────────────────┤
│      Sous-réseau Public     │      Sous-réseau Privé           │
│        10.0.1.0/24          │          10.0.2.0/24             │
│                             │                                   │
│  ┌─────────────────────┐    │    ┌─────────────────────┐        │
│  │   NAT Gateway       │    │    │   Instance EC2      │        │
│  │                     │    │    │   Application       │        │
│  │  - Dans subnet public│    │    │                     │        │
│  │  - IP Elastic       │    │    │  - Pas d'IP publique│        │
│  └─────────────────────┘    │    └─────────────────────┘        │
│          │                  │                │                  │
│  ┌───────┴───────┐          │        ┌───────┴───────┐          │
│  │ Internet      │          │        │ Route Table   │          │
│  │ Gateway       │◄─────────┼────────│  Privée       │          │
│  │               │          │        │               │          │
│  └───────────────┘          │        └───────────────┘          │
│                             │                │                  │
│  Route: 0.0.0.0/0 → igw     │        Route: 0.0.0.0/0 → nat     │
└─────────────────────────────┴───────────────────────────────────┘

Flux de données:
Instance Privée → NAT Gateway → Internet Gateway → Internet
Internet → Internet Gateway → ❌ (Bloqué par NAT) → Instance Privée
```

### 3.3. Route Tables - Schéma de Routage

#### Route Table Publique
```
┌─────────────────────────────────────────────────────────┐
│                Route Table Publique                     │
├──────────────┬─────────────┬─────────────┬─────────────┤
│  Destination │    Target   │   Statut    │  Propagé    │
├──────────────┼─────────────┼─────────────┼─────────────┤
│  10.0.0.0/16 │   local     │   Active    │     Non     │
│  0.0.0.0/0   │  igw-12345  │   Active    │     Non     │
└──────────────┴─────────────┴─────────────┴─────────────┘
        │
        └──► Associée aux sous-réseaux publics
```

#### Route Table Privée
```
┌─────────────────────────────────────────────────────────┐
│                Route Table Privée                       │
├──────────────┬─────────────┬─────────────┬─────────────┤
│  Destination │    Target   │   Statut    │  Propagé    │
├──────────────┼─────────────┼─────────────┼─────────────┤
│  10.0.0.0/16 │   local     │   Active    │     Non     │
│  0.0.0.0/0   │  nat-12345  │   Active    │     Non     │
│  10.1.0.0/16 │  pcx-67890  │   Active    │     Non     │
└──────────────┴─────────────┴─────────────┴─────────────┘
        │
        └──► Associée aux sous-réseaux privés
```

### 3.4. NACL vs Security Groups - Comparaison Visuelle

```
┌─────────────────────────────────┬─────────────────────────────────┐
│        NACL (Network ACL)       │      Security Groups            │
├─────────────────────────────────┼─────────────────────────────────┤
│  Niveau Sous-réseau             │  Niveau Instance (ENI)          │
│  Stateless                      │  Stateful                       │
│  Règles DENY/ALLOW              │  Règles ALLOW seulement         │
│  Évaluation par numéro          │  Évaluation de toutes les règles│
└─────────────────────────────────┴─────────────────────────────────┘

Exemple NACL:
┌─────────────────────────────────────────────────────────────────┐
│                   NACL - Sous-réseau Public                     │
├──────┬──────┬─────────┬──────────┬────────────┬─────────────────┤
│ Rule │ Type │ Protocol│ Port     │ Source     │     Action      │
├──────┼──────┼─────────┼──────────┼────────────┼─────────────────┤
│ 100  │ HTTP │   TCP   │    80    │ 0.0.0.0/0  │     ALLOW       │
│ 110  │ HTTPS│   TCP   │   443    │ 0.0.0.0/0  │     ALLOW       │
│ 120  │ SSH  │   TCP   │    22    │ 192.168.1.0│     ALLOW       │
│ *    │ ALL  │   ALL   │    ALL   │ 0.0.0.0/0  │     DENY        │
└──────┴──────┴─────────┴──────────┴────────────┴─────────────────┘

Exemple Security Group:
┌─────────────────────────────────────────────────────────────────┐
│                SG-WebServer (Stateful)                         │
├──────────────────┬──────────┬────────────┬─────────────────────┤
│     Type         │ Protocol │ Port Range │      Source         │
├──────────────────┼──────────┼────────────┼─────────────────────┤
│    HTTP          │   TCP    │     80     │      0.0.0.0/0      │
│    HTTPS         │   TCP    │    443     │      0.0.0.0/0      │
│    SSH           │   TCP    │     22     │    192.168.1.100    │
└──────────────────┴──────────┴────────────┴─────────────────────┘
```

### 3.5. VPC Peering - Architecture

```
┌─────────────────┐          Peering          ┌─────────────────┐
│   VPC A         │ ────────────────────────► │   VPC B         │
│  10.0.0.0/16    │         pcx-12345         │  10.1.0.0/16    │
│                 │ ◄──────────────────────── │                 │
└─────────────────┘                           └─────────────────┘
         │                                           │
         │                                           │
┌────────┴────────┐                         ┌────────┴────────┐
│  Route Table A  │                         │  Route Table B  │
├─────────────────┤                         ├─────────────────┤
│ 10.0.0.0/16 local│                         │ 10.1.0.0/16 local│
│ 10.1.0.0/16 pcx  │                         │ 10.0.0.0/16 pcx  │
└─────────────────┘                         └─────────────────┘

ATTENTION: Pas de transitivité
VPC A ↔ VPC B ↔ VPC C  n'implique PAS  VPC A ↔ VPC C
```

---

## 4. Architectures Avancées

### 4.1. Architecture Three-Tier Complète

```
┌─────────────────────────────────────────────────────────────────────────┐
│                            VPC: 10.0.0.0/16                            │
├───────────────┬───────────────┬───────────────┬───────────────┬─────────┤
│  Web Tier     │  App Tier     │  Data Tier    │  Management   │ NAT     │
│  (Public)     │  (Privé)      │  (Privé)      │  (Public)     │ GW      │
├───────────────┼───────────────┼───────────────┼───────────────┼─────────┤
│ AZ A:10.0.1.0/24│ AZ A:10.0.11.0/24│ AZ A:10.0.21.0/24│ AZ A:10.0.31.0/24│ AZ A   │
│ AZ B:10.0.2.0/24│ AZ B:10.0.12.0/24│ AZ B:10.0.22.0/24│ AZ B:10.0.32.0/24│ AZ B   │
└───────────────┴───────────────┴───────────────┴───────────────┴─────────┘
        │               │               │               │         │
        │               │               │               │         │
┌───────┴───────┐ ┌─────┴─────┐ ┌───────┴───────┐ ┌─────┴─────┐ ┌─┴─┐
│  Application  │ │  Application│ │   Database   │ │  Bastion  │ │NAT│
│  Load         │ │   Servers   │ │   Servers    │ │   Host    │ │GW │
│  Balancer     │ │             │ │              │ │           │ │   │
└───────┬───────┘ └─────────────┘ └───────────────┘ └───────────┘ └─┬─┘
        │               │               │               │           │
        └───────────────┼───────────────┼───────────────┼───────────┘
                        │               │               │
                  ┌─────┴─────┐   ┌─────┴─────┐   ┌─────┴─────┐
                  │  Security │   │  Security │   │  Security │
                  │  Groups   │   │  Groups   │   │  Groups   │
                  └───────────┘   └───────────┘   └───────────┘

Flux Autorisés:
Internet → ALB → App Servers → Database
Admin → Bastion Host → App/Database Servers
App Servers → NAT GW → Internet (updates)
```

### 4.2. Architecture Multi-AZ avec Haute Disponibilité

```
                          ┌─────────────────┐
                          │   Internet      │
                          └────────┬────────┘
                                   │
                   ┌───────────────┼───────────────┐
                   │               │               │
           ┌───────┴───────┐ ┌─────┴─────┐ ┌───────┴───────┐
           │  Availability │ │Availability│ │ Availability │
           │     Zone A    │ │   Zone B   │ │    Zone C    │
           └───────────────┘ └────────────┘ └───────────────┘
                   │               │               │
           ┌───────┴───────┐ ┌─────┴─────┐ ┌───────┴───────┐
           │  Public       │ │ Public    │ │  Public       │
           │  Subnet       │ │ Subnet    │ │  Subnet       │
           │  10.0.1.0/24  │ │10.0.2.0/24│ │ 10.0.3.0/24  │
           └───────┬───────┘ └─────┬─────┘ └───────┬───────┘
                   │               │               │
           ┌───────┴───────┐ ┌─────┴─────┐ ┌───────┴───────┐
           │  NAT Gateway  │ │ NAT Gateway│ │  NAT Gateway │
           │     AZ A      │ │   AZ B     │ │    AZ C      │
           └───────┬───────┘ └─────┬─────┘ └───────┬───────┘
                   │               │               │
           ┌───────┴───────┐ ┌─────┴─────┐ ┌───────┴───────┐
           │  Private      │ │ Private   │ │  Private      │
           │  Subnet       │ │ Subnet    │ │  Subnet       │
           │  10.0.11.0/24 │ │10.0.12.0/24│ │10.0.13.0/24  │
           └───────┬───────┘ └─────┬─────┘ └───────┬───────┘
                   │               │               │
           ┌───────┴───────┐ ┌─────┴─────┐ ┌───────┴───────┐
           │  Application  │ │Application│ │  Application  │
           │   Servers     │ │ Servers   │ │   Servers     │
           └───────────────┘ └────────────┘ └───────────────┘
```

### 4.3. VPC avec Endpoints - Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      VPC: 10.0.0.0/16                          │
├─────────────────────────────┬───────────────────────────────────┤
│    Sous-réseau Privé        │      Connectivité Services AWS   │
│       10.0.1.0/24           │                                  │
│                             │                                  │
│  ┌─────────────────────┐    │    ┌─────────────────────────┐   │
│  │   Instance EC2      │    │    │   VPC Endpoints         │   │
│  │                     │    │    │                         │   │
│  │  - Application      │────┼───►│  ┌─────────────────┐    │   │
│  │  - Pas d'Internet   │    │    │  │ S3 Endpoint     │───┼───┼──► S3
│  └─────────────────────┘    │    │  │ (Gateway)       │    │   │
│                             │    │  └─────────────────┘    │   │
│                             │    │                         │   │
│                             │    │  ┌─────────────────┐    │   │
│                             │    │  │ SSM Endpoint    │───┼───┼──► SSM
│                             │    │  │ (Interface)     │    │   │
│                             │    │  └─────────────────┘    │   │
│                             │    │                         │   │
│                             │    │  ┌─────────────────┐    │   │
│                             │    │  │ DynamoDB        │───┼───┼──► DynamoDB
│                             │    │  │ Endpoint        │    │   │
│                             │    │  └─────────────────┘    │   │
└─────────────────────────────┴───────────────────────────────────┘

Avantages:
• Pas de frais de transfert de données
• Sécurité améliorée (pas d'Internet)
• Performance réseau AWS
```

---

## 5. Sécurité et Bonnes Pratiques

### 5.1. Stratégie de Sécurité en Couches

```
┌─────────────────────────────────────────────────────────────────┐
│                    Stratégie de Sécurité Multi-couches         │
├─────────────────┬───────────────────────────────────────────────┤
│     Couche      │                Éléments                      │
├─────────────────┼───────────────────────────────────────────────┤
│  Application    │ • Chiffrement des données                    │
│                 │ • Authentification forte                     │
│                 │ • Gestion des sessions                       │
├─────────────────┼───────────────────────────────────────────────┤
│     IAM         │ • Politiques IAM least privilege            │
│                 │ • Roles EC2                                 │
│                 │ • MFA                                       │
├─────────────────┼───────────────────────────────────────────────┤
│   Host/OS       │ • Hardening du OS                           │
│                 │ • Patch management                          │
│                 │ • Antivirus/Malware protection              │
├─────────────────┼───────────────────────────────────────────────┤
│  Security Groups│ • Règles stateful                           │
│                 │ • Least privilege                           │
│                 │ • Références par SG (pas IP)                │
├─────────────────┼───────────────────────────────────────────────┤
│      NACL       │ • Règles stateless                          │
│                 │ • Protection sous-réseau                    │
│                 │ • Règles deny explicites                    │
├─────────────────┼───────────────────────────────────────────────┤
│   Segmentation  │ • Sous-réseaux séparés                      │
│                 │ • Route tables différentes                  │
│                 │ • VPC peering contrôlé                      │
└─────────────────┴───────────────────────────────────────────────┘
```

### 5.2. Design de Sécurité Réseau

```
┌─────────────────────────────────────────────────────────────────┐
│                  Architecture Sécurisée                        │
├─────────────────┬─────────────────┬─────────────────┬───────────┤
│   DMZ/Public    │    Application  │     Données      │  Management│
│                 │                 │                 │           │
│ 10.0.1.0/24     │  10.0.11.0/24   │  10.0.21.0/24   │10.0.31.0/24│
├─────────────────┼─────────────────┼─────────────────┼───────────┤
│ • ALB/ELB       │ • App Servers   │ • Databases     │ • Bastion │
│ • NAT Gateway   │ • API Servers   │ • Cache         │ • Monitoring│
│ • WAF           │ • Microservices │ • File Storage  │ • Jumpbox │
├─────────────────┼─────────────────┼─────────────────┼───────────┤
│ NACL:           │ NACL:           │ NACL:           │ NACL:     │
│ - HTTP/HTTPS IN │ - App Ports IN  │ - DB Ports IN   │ - SSH IN  │
│ - Ephemeral OUT │ - From Web ONLY │ - From App ONLY │ - From Office│
└─────────────────┴─────────────────┴─────────────────┴───────────┘

Flux Autorisés:
Internet → DMZ → Application → Données
Office → Management → Application/Données
```

---

## 6. Monitoring et Troubleshooting

### 6.1. VPC Flow Logs - Analyse des Données

```
Format des Logs:
version account-id interface-id srcaddr dstaddr srcport dstport protocol packets bytes start end action log-status

Exemple de Log:
2 123456789012 eni-123456 10.0.1.20 10.0.2.30 34567 80 6 25 5200 1432917020 1432917080 ACCEPT OK

┌─────────────────────────────────────────────────────────────────┐
│                      Analyse Flow Logs                         │
├──────────────┬─────────────────────────────────────────────────┤
│   Champ      │                Description                      │
├──────────────┼─────────────────────────────────────────────────┤
│ version      │ Version du format (2)                          │
│ account-id   │ ID du compte AWS                               │
│ interface-id │ ID de l'interface réseau                       │
│ srcaddr      │ Adresse IP source                              │
│ dstaddr      │ Adresse IP destination                         │
│ srcport      │ Port source                                    │
│ dstport      │ Port destination                               │
│ protocol     │ Numéro de protocol (6=TCP, 17=UDP)             │
│ packets      │ Nombre de paquets                              │
│ bytes        │ Nombre d'octets                                │
│ start        │ Heure de début (timestamp)                     │
│ end          │ Heure de fin (timestamp)                       │
│ action       │ ACCEPT ou REJECT                               │
│ log-status   │ Statut du log (OK, NODATA, SKIPDATA)           │
└──────────────┴─────────────────────────────────────────────────┘
```

### 6.2. Troubleshooting - Flowchart de Diagnostic

```
┌─────────────────┐
│  Problème:      │
│  Connectivité   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Instance        │
│ Running?        │───Non──► Démarrer l'instance
└────────┬────────┘
         │Oui
         ▼
┌─────────────────┐
│ Security Groups │
│ Configurés?     │───Non──► Autoriser le trafic
└────────┬────────┘
         │Oui
         ▼
┌─────────────────┐
│ NACL Rules      │
│ Permettent?     │───Non──► Ajouter règles NACL
└────────┬────────┘
         │Oui
         ▼
┌─────────────────┐
│ Route Table     │
│ Correcte?       │───Non──► Corriger les routes
└────────┬────────┘
         │Oui
         ▼
┌─────────────────┐
│ VPC Flow Logs   │
│ Trafic bloqué?  │───Oui──► Analyser et corriger
└────────┬────────┘
         │Non
         ▼
┌─────────────────┐
│   Résolu!       │
└─────────────────┘
```

### 6.3. Dashboard de Monitoring Recommandé

```
┌─────────────────────────────────────────────────────────────────┐
│                  Dashboard VPC Monitoring                      │
├─────────────────┬─────────────────┬─────────────────┬───────────┤
│   Métriques     │    Web Tier     │    App Tier     │ Data Tier │
├─────────────────┼─────────────────┼─────────────────┼───────────┤
│ NetworkIn       │ ████ 1.2 GB     │ ███ 800 MB      │ ██ 400 MB │
│ NetworkOut      │ █████ 2.1 GB    │ ████ 1.1 GB     │ █ 150 MB  │
│ PacketDropCount │ █ 5             │ █ 3             │ 0         │
│ ActiveFlowCount │ ████ 450        │ ███ 320         │ ██ 120    │
└─────────────────┴─────────────────┴─────────────────┴───────────┘

Alertes Configurées:
• PacketDropCount > 100/heure
• NetworkIn > 5 GB/heure
• REJECT actions > 50/heure
```

---

## 7. Checklist de Déploiement Complet

### 7.1. Diagramme de Gantt - Plan de Déploiement

```
Phase           │ Semaine 1 │ Semaine 2 │ Semaine 3 │ Semaine 4 │
────────────────┼───────────┼───────────┼───────────┼───────────┤
Planification   │ █████████████████████████████████████████████ │
Conception      │           │ █████████████████████████████████ │
Déploiement VPC │           │           │ █████████████████████ │
Configuration   │           │           │           │ █████████ │
Testing         │           │           │           │ █████████ │
```

### 7.2. Matrice de Décision - Choix d'Architecture

```
┌─────────────────┬────────────┬────────────┬────────────┬────────────┐
│   Scénario      │ Single AZ  │ Multi-AZ   │ Multi-Region│ Hybride   │
├─────────────────┼────────────┼────────────┼────────────┼────────────┤
│  Development    │     ✅     │     🟡     │     ❌     │     🟡     │
│  Testing        │     🟡     │     ✅     │     ❌     │     🟡     │
│  Production     │     ❌     │     ✅     │     🟡     │     ✅     │
│  Disaster Recovery│     ❌     │     🟡     │     ✅     │     ✅     │
│  Global App     │     ❌     │     ❌     │     ✅     │     ✅     │
└─────────────────┴────────────┴────────────┴────────────┴────────────┘

✅ = Recommandé   🟡 = Possible   ❌ = Non recommandé
```

## Conclusion

Ce cours visuel complet vous a présenté tous les aspects des VPC AWS avec des diagrammes détaillés pour mieux comprendre les concepts. Les éléments clés à retenir sont :

### Architecture Recommandée pour Production
```
┌─────────────────────────────────────────────────────────────────┐
│                 ARCHITECTURE VPC PRODUCTION                    │
├─────────────────┬─────────────────┬─────────────────┬───────────┤
│   Web Tier      │   App Tier      │  Data Tier      │  Mgmt     │
│ (Multi-AZ)      │ (Multi-AZ)      │ (Multi-AZ)      │ (Single AZ)│
├─────────────────┼─────────────────┼─────────────────┼───────────┤
│ • ALB Public    │ • EC2 Privé     │ • RDS Multi-AZ  │ • Bastion │
│ • WAF           │ • Auto Scaling  │ • Elasticache   │ • NAT GW  │
│ • NACL: HTTP/S  │ • NACL: App     │ • NACL: DB      │ • Monitoring│
│ • SG: Web       │ • SG: App       │ • SG: Data      │ • SG: Mgmt│
└─────────────────┴─────────────────┴─────────────────┴───────────┘
```

### Règles d'Or pour les VPC
1. **Planifiez large** - Utilisez /16 ou plus grand pour le VPC
2. **Segmentez logiquement** - Séparation Web/App/Data
3. **Multi-AZ toujours** - Pour la haute disponibilité
4. **Security First** - Principe du moindre privilège
5. **Monitorer tout** - VPC Flow Logs + CloudWatch
6. **Automatisez** - Terraform/CloudFormation
7. **Documentez** - Diagrammes et procédures

