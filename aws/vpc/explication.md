# Cours Complet et Détaillé sur les VPC AWS

## Table des Matières
1. [Introduction aux VPC](#introduction-aux-vpc)
2. [Concepts Fondamentaux de Réseau](#concepts-fondamentaux-de-réseau)
3. [Composants Détaillés du VPC](#composants-détails-du-vpc)
4. [Architectures Avancées](#architectures-avancées)
5. [Sécurité et Bonnes Pratiques](#sécurité-et-bonnes-pratiques)
6. [Monitoring et Troubleshooting](#monitoring-et-troubleshooting)

---

## 1. Introduction aux VPC

### 1.1. Définition d'un VPC

**VPC (Virtual Private Cloud)** : C'est un réseau virtuel isolé et sécurisé dans le cloud AWS où vous pouvez déployer vos ressources informatiques. C'est l'équivalent d'un datacenter virtuel dans le cloud.

**Analogie** : Imaginez un VPC comme un immeuble virtuel :
- Le VPC = l'immeuble entier
- Les sous-réseaux = les différents étages
- Les instances EC2 = les appartements
- Les Security Groups = les serrures des portes

### 1.2. Caractéristiques Principales

- **Isolation complète** : Chaque VPC est isolé des autres VPC
- **Contrôle total** sur la configuration réseau
- **Flexibilité** dans le choix des plages IP
- **Sécurité avancée** avec multiples couches de protection
- **Connectivité** avec votre réseau on-premise

---

## 2. Concepts Fondamentaux de Réseau

### 2.1. Adressage IP et CIDR

#### Adresses IP IPv4
- Format : 4 octets (ex: 192.168.1.1)
- Chaque octet va de 0 à 255
- Parties : Network ID + Host ID

#### Notation CIDR (Classless Inter-Domain Routing)
**Format** : IP/Préfixe (ex: 10.0.0.0/16)

**Masque de sous-réseau** :
- /16 = 255.255.0.0
- /24 = 255.255.255.0
- /32 = 255.255.255.255

#### Calcul du nombre d'adresses IP

**Formule** : 2^(32 - préfixe) - 5 adresses réservées

**Exemples de calcul** :
```bash
/16 : 2^(32-16) = 2^16 = 65,536 adresses
/24 : 2^(32-24) = 2^8 = 256 adresses
/28 : 2^(32-28) = 2^4 = 16 adresses
```

#### Adresses réservées dans un sous-réseau AWS
Dans chaque sous-réseau, AWS réserve 5 adresses IP :
- **.0** : Adresse réseau
- **.1** : Routeur VPC (Gateway par défaut)
- **.2** : Réservé pour DNS AWS
- **.3** : Réservé pour usage futur
- **.255** : Adresse de broadcast

**Exemple pour 10.0.1.0/24** :
- Plage utilisable : 10.0.1.0 - 10.0.1.255
- Adresses réservées : 10.0.1.0, 10.0.1.1, 10.0.1.2, 10.0.1.3, 10.0.1.255
- Première adresse utilisable : 10.0.1.4
- Dernière adresse utilisable : 10.0.1.254

### 2.2. Plages IP Privées (RFC 1918)

```bash
# Plages IP privées recommandées
10.0.0.0 - 10.255.255.255     (10.0.0.0/8)
172.16.0.0 - 172.31.255.255   (172.16.0.0/12)
192.168.0.0 - 192.168.255.255 (192.168.0.0/16)
```

---

## 3. Composants Détaillés du VPC

### 3.1. VPC (Virtual Private Cloud)

#### Définition
C'est le conteneur réseau principal qui isole vos ressources des autres clients AWS.

#### Configuration
```bash
# Exemple de création avec AWS CLI
aws ec2 create-vpc \
    --cidr-block 10.0.0.0/16 \
    --instance-tenancy default
```

#### Attributs importants
- **CIDR Block** : Plage IP principale
- **Tenancy** : default ou dedicated
- **DNS Resolution** : Résolution DNS interne
- **DNS Hostnames** : Noms d'hôtes pour les instances

### 3.2. Sous-réseaux (Subnets)

#### Définition
Un sous-réseau est une subdivision logique du VPC dans une Availability Zone spécifique.

#### Types de sous-réseaux

**Public** :
- Route vers l'Internet Gateway
- Peut avoir des IPs publiques
- Utilisé pour les load balancers, NAT Gateways

**Privé** :
- Route vers le NAT Gateway
- Pas d'accès internet direct
- Utilisé pour les bases de données, applications

**Isolé** :
- Pas de route vers internet
- Utilisé pour les données sensibles

#### Calcul et création de sous-réseaux

**Exemple de plan d'adressage** :
```bash
VPC: 10.0.0.0/16 (65,536 adresses)

# Sous-réseaux publics (2 AZs)
Public Subnet AZ A: 10.0.1.0/24 (256 adresses)
Public Subnet AZ B: 10.0.2.0/24 (256 adresses)

# Sous-réseaux privés (2 AZs)  
Private Subnet AZ A: 10.0.11.0/24 (256 adresses)
Private Subnet AZ B: 10.0.12.0/24 (256 adresses)

# Sous-réseaux données (2 AZs)
Data Subnet AZ A: 10.0.21.0/24 (256 adresses)
Data Subnet AZ B: 10.0.22.0/24 (256 adresses)
```

**Création d'un sous-réseau** :
```bash
aws ec2 create-subnet \
    --vpc-id vpc-123456 \
    --cidr-block 10.0.1.0/24 \
    --availability-zone us-east-1a
```

### 3.3. Internet Gateway (IGW)

#### Définition
Composant horizontalement scalable et redondant qui permet la communication entre votre VPC et internet.

#### Caractéristiques
- **Redondant et hautement disponible** par défaut
- **Une seule IGW par VPC** (mais un VPC peut fonctionner sans IGW)
- **Ne cause pas de goulot d'étranglement** de bande passante

#### Configuration
```bash
# Création et attachement
aws ec2 create-internet-gateway
aws ec2 attach-internet-gateway \
    --vpc-id vpc-123456 \
    --internet-gateway-id igw-123456
```

### 3.4. NAT Gateway (Network Address Translation)

#### Définition
Permet aux instances dans les sous-réseaux privés d'initier des connexions sortantes vers internet tout en bloquant les connexions entrantes non sollicitées.

#### Types de NAT

**NAT Gateway** (Recommandé) :
- Managed service par AWS
- Haute disponibilité dans une AZ
- Jusqu'à 45 Gbps de bande passante
- Tarification : heure + données traitées

**NAT Instance** :
- Instance EC2 avec software NAT
- Nécessite gestion manuelle
- Moins cher pour petits trafics
- Configuration manuelle de la haute disponibilité

#### Placement du NAT Gateway
```bash
# Le NAT Gateway doit être dans un sous-réseau PUBLIC
# avec une route vers l'Internet Gateway

# Route Table pour sous-réseaux privés
Destination    Cible
10.0.0.0/16   local
0.0.0.0/0     nat-123456  # NAT Gateway
```

#### Création d'un NAT Gateway
```bash
# Allouer une IP Elastic
aws ec2 allocate-address --domain vpc

# Créer le NAT Gateway
aws ec2 create-nat-gateway \
    --subnet-id subnet-123456 \
    --allocation-id eipalloc-123456
```

### 3.5. Route Tables

#### Définition
Table de routage qui détermine où le trafic réseau est dirigé.

#### Composants d'une route
- **Destination** : Plage CIDR de destination
- **Target** : Cible pour atteindre la destination
- **Propagation** : Propagation des routes VPN (optionnel)

#### Types de Route Tables

**Main Route Table** :
- Créée automatiquement avec le VPC
- Associée par défaut à tous les sous-réseaux

**Custom Route Tables** :
- Créées manuellement
- Associations explicites aux sous-réseaux

#### Exemples de configurations

**Route Table Publique** :
```bash
Destination      Target          Description
10.0.0.0/16     local           Communication intra-VPC
0.0.0.0/0       igw-123456      Accès internet
```

**Route Table Privée** :
```bash
Destination      Target          Description  
10.0.0.0/16     local           Communication intra-VPC
0.0.0.0/0       nat-123456      Accès internet via NAT
```

**Route Table pour VPC Peering** :
```bash
Destination      Target          Description
10.0.0.0/16     local           VPC local
10.1.0.0/16     pcx-123456      VPC peeré
0.0.0.0/0       nat-123456      Internet
```

### 3.6. NACL (Network Access Control Lists)

#### Définition
Liste de contrôle d'accès stateless qui fonctionne au niveau du sous-réseau. C'est un firewall optionnel pour contrôler le trafic entrant et sortant des sous-réseaux.

#### Caractéristiques des NACLs
- **Stateless** : Les règles entrantes/sortantes sont indépendantes
- **Évaluation par numéro** (de 1 à 32766, plus petit d'abord)
- **Règles DENY et ALLOW**
- **Appliqué au niveau sous-réseau**
- **Une NACL par défaut par VPC**

#### Structure d'une règle NACL
```bash
Rule # | Type | Protocol | Port Range | Source | Allow/Deny
```

#### Exemple de configuration NACL

**NACL pour sous-réseau public** :
```bash
# Règles entrantes (Inbound)
Rule # | Type      | Protocol | Port | Source       | Action
100    | SSH       | TCP      | 22   | 203.0.113.1/32 | ALLOW
110    | HTTP      | TCP      | 80   | 0.0.0.0/0    | ALLOW  
111    | HTTPS     | TCP      | 443  | 0.0.0.0/0    | ALLOW
120    | Ephemeral | TCP      | 1024-65535 | 0.0.0.0/0 | ALLOW
*      | ALL       | ALL      | ALL  | 0.0.0.0/0    | DENY

# Règles sortantes (Outbound)
Rule # | Type      | Protocol | Port | Destination  | Action
100    | HTTP      | TCP      | 80   | 0.0.0.0/0    | ALLOW
110    | HTTPS     | TCP      | 443  | 0.0.0.0/0    | ALLOW
120    | Ephemeral | TCP      | 1024-65535 | 0.0.0.0/0 | ALLOW
*      | ALL       | ALL      | ALL  | 0.0.0.0/0    | DENY
```

**NACL pour sous-réseau privé** :
```bash
# Règles entrantes
Rule # | Type      | Protocol | Port | Source       | Action
100    | SSH       | TCP      | 22   | 10.0.1.0/24  | ALLOW
110    | Custom    | TCP      | 8080 | 10.0.1.0/24  | ALLOW
120    | Ephemeral | TCP      | 1024-65535 | 10.0.0.0/16 | ALLOW
*      | ALL       | ALL      | ALL  | 0.0.0.0/0    | DENY

# Règles sortantes  
Rule # | Type      | Protocol | Port | Destination  | Action
100    | HTTP      | TCP      | 80   | 0.0.0.0/0    | ALLOW
110    | HTTPS     | TCP      | 443  | 0.0.0.0/0    | ALLOW
120    | Ephemeral | TCP      | 1024-65535 | 10.0.0.0/16 | ALLOW
*      | ALL       | ALL      | ALL  | 0.0.0.0/0    | DENY
```

### 3.7. Security Groups

#### Définition
Firewall stateful au niveau de l'instance (ENI) qui contrôle le trafic entrant et sortant.

#### Caractéristiques des Security Groups
- **Stateful** : Si une requête entrante est autorisée, la réponse est automatiquement autorisée
- **Règles ALLOW uniquement** (tout est DENY par défaut)
- **Associé aux instances** (ENI level)
- **Une instance peut avoir multiple SGs**

#### Exemples de Security Groups

**SG pour serveur web** :
```bash
# Règles entrantes
Type    | Protocol | Port | Source       | Description
HTTP    | TCP      | 80   | 0.0.0.0/0    | Accès web public
HTTPS   | TCP      | 443  | 0.0.0.0/0    | Accès HTTPS public
SSH     | TCP      | 22   | 203.0.113.1/32 | Admin SSH

# Règles sortantes (optionnelles - tout autorisé par défaut)
Type    | Protocol | Port | Destination  | Description
All     | All      | All  | 0.0.0.0/0    | Accès sortant complet
```

**SG pour base de données** :
```bash
# Règles entrantes
Type    | Protocol | Port | Source       | Description
MySQL   | TCP      | 3306 | 10.0.1.0/24  | Accès depuis app servers
MySQL   | TCP      | 3306 | 10.0.2.0/24  | Accès depuis app servers

# Règles sortantes
Type    | Protocol | Port | Destination  | Description
All     | All      | All  | 0.0.0.0/0    | Tout autorisé
```

### 3.8. VPC Endpoints

#### Définition
Permet une connectivité privée entre votre VPC et les services AWS sans passer par internet.

#### Types de VPC Endpoints

**Interface Endpoints** (ENI) :
- Services comme S3, DynamoDB
- Utilise PrivateLink
- Coût par heure + données

**Gateway Endpoints** :
- Services S3 et DynamoDB uniquement
- Gratuit
- Ajoute une route dans la route table

#### Configuration Gateway Endpoint
```bash
aws ec2 create-vpc-endpoint \
    --vpc-id vpc-123456 \
    --service-name com.amazonaws.us-east-1.s3 \
    --route-table-ids rtb-123456
```

### 3.9. VPC Peering

#### Définition
Connexion one-to-one entre deux VPCs permettant le routage privé utilisant l'infrastructure AWS.

#### Règles importantes
- **Pas de relations transitives** : A ↔ B ↔ C ne permet pas A ↔ C
- **Pas de chevauchement de CIDR**
- **Peering inter-région possible**

#### Configuration
```bash
# Créer la requête de peering
aws ec2 create-vpc-peering-connection \
    --vpc-id vpc-123456 \
    --peer-vpc-id vpc-789012

# Accepter la requête
aws ec2 accept-vpc-peering-connection \
    --vpc-peering-connection-id pcx-123456
```

---

## 4. Architectures Avancées

### 4.1. Architecture Three-Tier Classique

```bash
VPC: 10.0.0.0/16

# Tier Web (Public)
Web Subnet AZ A: 10.0.1.0/24
Web Subnet AZ B: 10.0.2.0/24
→ Route: 0.0.0.0/0 → IGW
→ NACL: HTTP/HTTPS entrant

# Tier Application (Privé)
App Subnet AZ A: 10.0.11.0/24  
App Subnet AZ B: 10.0.12.0/24
→ Route: 0.0.0.0/0 → NAT Gateway
→ NACL: SSH depuis Web Tier seulement

# Tier Données (Privé)
Data Subnet AZ A: 10.0.21.0/24
Data Subnet AZ B: 10.0.22.0/24
→ Route: 0.0.0.0/0 → NAT Gateway
→ NACL: DB ports depuis App Tier seulement
```

### 4.2. Architecture avec VPC Endpoints

```bash
VPC: 10.0.0.0/16

# Sous-réseaux privés
Private Subnets: 10.0.1.0/24, 10.0.2.0/24

# VPC Endpoints
→ S3 Gateway Endpoint (gratuit)
→ DynamoDB Gateway Endpoint (gratuit)  
→ SSM Interface Endpoint (payant)
→ CloudWatch Logs Interface Endpoint (payant)

# Routes pour endpoints
10.0.1.0/24 → local
pl-svc → vpce-123456  # Pour les Interface Endpoints
```

### 4.3. Architecture Multi-VPC (Hub-and-Spoke)

```bash
# VPC Hub (Services partagés)
Hub VPC: 10.0.0.0/16
→ DNS, Active Directory, Monitoring

# VPC Spoke (Environnements)
Prod VPC: 10.1.0.0/16   ↔ Hub VPC
Dev VPC: 10.2.0.0/16    ↔ Hub VPC  
DMZ VPC: 10.3.0.0/16    ↔ Hub VPC

# Transit Gateway (Alternative moderne)
tgw-123456 connecte tous les VPCs
```

---

## 5. Sécurité et Bonnes Pratiques

### 5.1. Stratégie de Sécurité en Couches

```bash
# Couche 1: NACL (Niveau sous-réseau)
# Couche 2: Security Groups (Niveau instance)  
# Couche 3: Configuration OS (Niveau système)
# Couche 4: IAM (Contrôle d'accès)
# Couche 5: Chiffrement (Données au repos/en transit)
```

### 5.2. Bonnes Pratiques de Conception

#### Planification des Adresses IP
```bash
# Mauvaise pratique
10.0.1.0/24, 10.0.2.0/24, 10.0.3.0/24...

# Bonne pratique - Prévoir la croissance
10.0.0.0/16 divisé en blocs /19:
- Web:     10.0.0.0/19     (8,192 adresses)
- App:     10.0.32.0/19    (8,192 adresses) 
- Data:    10.0.64.0/19    (8,192 adresses)
- Reserved: 10.0.96.0/19   (8,192 adresses)
```

#### Haute Disponibilité
```bash
# NAT Gateway par AZ
NAT Gateway AZ A → Private Subnets AZ A
NAT Gateway AZ B → Private Subnets AZ B

# Load Balancers multi-AZ
ALB dans 2+ sous-réseaux publics
```

### 5.3. Hardening du VPC

#### Configuration sécurisée
```bash
# 1. Activer VPC Flow Logs
# 2. Désactiver DNS hostnames si non nécessaire
# 3. Utiliser des Security Groups restrictifs
# 4. Implémenter le principe du moindre privilège
# 5. Configurer des NACLs restrictives
```

#### Monitoring de sécurité
```bash
# Services AWS à utiliser
- AWS CloudTrail (logs API)
- VPC Flow Logs (trafic réseau)
- AWS Security Hub (vue sécurité unifiée)
- AWS Config (conformité des ressources)
- GuardDuty (détection menaces)
```

---

## 6. Monitoring et Troubleshooting

### 6.1. VPC Flow Logs

#### Définition
Capture les informations sur le trafic IP entrant et sortant des interfaces réseau dans votre VPC.

#### Types de Flow Logs
- **VPC Level** : Toutes les ENIs dans le VPC
- **Subnet Level** : Toutes les ENIs dans le sous-réseau  
- **ENI Level** : Interface réseau spécifique

#### Format des logs
```bash
version account-id interface-id srcaddr dstaddr srcport dstport protocol packets bytes start end action log-status
2 123456789012 eni-123456 10.0.1.4 10.0.2.6 45678 80 6 25 16200 1432917820 1432917880 ACCEPT OK
```

#### Configuration
```bash
aws ec2 create-flow-logs \
    --resource-type VPC \
    --resource-id vpc-123456 \
    --traffic-type ALL \
    --log-destination-type cloud-watch-logs \
    --log-group-name VPCFlowLogs \
    --deliver-logs-permission-arn arn:aws:iam::123456789012:role/FlowLogsRole
```

### 6.2. Troubleshooting Courant

#### Problèmes de connectivité - Checklist
```bash
1. ✅ Vérifier l'état de l'instance (running)
2. ✅ Vérifier les Security Groups (règles entrantes/sortantes)
3. ✅ Vérifier les NACLs (règles par numéro)
4. ✅ Vérifier les Route Tables (routes correctes)
5. ✅ Vérifier les VPC Flow Logs (trafic bloqué)
6. ✅ Vérifier les IGW/NAT Gateway (états)
7. ✅ Tester depuis différentes sources
```

#### Commandes de diagnostic
```bash
# Test de connectivité de base
ping <ip-destination>
telnet <ip> <port>
nc -zv <ip> <port>
traceroute <destination>

# Vérification configuration AWS
aws ec2 describe-instances --instance-ids i-123456
aws ec2 describe-security-groups --group-ids sg-123456
aws ec2 describe-route-tables --route-table-ids rtb-123456
```

### 6.3. Outils de Monitoring

#### CloudWatch Metrics
```bash
# Métriques importantes
- NetworkIn, NetworkOut (bytes)
- PacketDropCount (paquets dropés)
- NewFlowCount, ActiveFlowCount (flows)
- Bandwidth (bande passante utilisée)
```

#### CloudWatch Logs Insights pour VPC Flow Logs
```bash
# Requêtes utiles
# Top 10 destinations par trafic
stats sum(bytes) as totalBytes by dstAddr
| sort totalBytes desc
| limit 10

# Trafic rejeté
filter action="REJECT"
| stats count() as rejectCount by srcAddr, dstAddr, dstPort
```

---

## 7. Automatisation avec Terraform (Complet)

### 7.1. Configuration Terraform Complète

```hcl
# variables.tf
variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "availability_zones" {
  description = "List of availability zones"
  type        = list(string)
  default     = ["us-east-1a", "us-east-1b"]
}

# main.tf - VPC
resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true
  
  tags = {
    Name = "production-vpc"
  }
}

# Internet Gateway
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id
  
  tags = {
    Name = "main-igw"
  }
}

# Sous-réseaux publics
resource "aws_subnet" "public" {
  count                   = length(var.availability_zones)
  vpc_id                  = aws_vpc.main.id
  cidr_block              = cidrsubnet(aws_vpc.main.cidr_block, 8, count.index)
  availability_zone       = var.availability_zones[count.index]
  map_public_ip_on_launch = true
  
  tags = {
    Name = "public-subnet-${count.index + 1}"
    Tier = "Public"
  }
}

# Sous-réseaux privés
resource "aws_subnet" "private" {
  count             = length(var.availability_zones)
  vpc_id            = aws_vpc.main.id
  cidr_block        = cidrsubnet(aws_vpc.main.cidr_block, 8, count.index + 10)
  availability_zone = var.availability_zones[count.index]
  
  tags = {
    Name = "private-subnet-${count.index + 1}"
    Tier = "Private"
  }
}

# NAT Gateways
resource "aws_eip" "nat" {
  count = length(var.availability_zones)
  domain = "vpc"
}

resource "aws_nat_gateway" "main" {
  count         = length(var.availability_zones)
  allocation_id = aws_eip.nat[count.index].id
  subnet_id     = aws_subnet.public[count.index].id
  
  tags = {
    Name = "nat-gateway-${count.index + 1}"
  }
  
  depends_on = [aws_internet_gateway.main]
}

# Route Tables
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id
  
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }
  
  tags = {
    Name = "public-rt"
  }
}

resource "aws_route_table" "private" {
  count = length(var.availability_zones)
  
  vpc_id = aws_vpc.main.id
  
  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.main[count.index].id
  }
  
  tags = {
    Name = "private-rt-${count.index + 1}"
  }
}

# Associations des Route Tables
resource "aws_route_table_association" "public" {
  count          = length(aws_subnet.public)
  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table_association" "private" {
  count          = length(aws_subnet.private)
  subnet_id      = aws_subnet.private[count.index].id
  route_table_id = aws_route_table.private[count.index].id
}

# NACLs
resource "aws_network_acl" "public" {
  vpc_id     = aws_vpc.main.id
  subnet_ids = aws_subnet.public[*].id
  
  # Règles entrantes
  ingress {
    protocol   = "tcp"
    rule_no    = 100
    action     = "allow"
    cidr_block = "0.0.0.0/0"
    from_port  = 80
    to_port    = 80
  }
  
  ingress {
    protocol   = "tcp"
    rule_no    = 110
    action     = "allow"
    cidr_block = "0.0.0.0/0"
    from_port  = 443
    to_port    = 443
  }
  
  ingress {
    protocol   = "tcp"
    rule_no    = 120
    action     = "allow"
    cidr_block = "0.0.0.0/0"
    from_port  = 1024
    to_port    = 65535
  }
  
  # Règles sortantes
  egress {
    protocol   = "tcp"
    rule_no    = 100
    action     = "allow"
    cidr_block = "0.0.0.0/0"
    from_port  = 80
    to_port    = 80
  }
  
  egress {
    protocol   = "tcp"
    rule_no    = 110
    action     = "allow"
    cidr_block = "0.0.0.0/0"
    from_port  = 443
    to_port    = 443
  }
  
  egress {
    protocol   = "tcp"
    rule_no    = 120
    action     = "allow"
    cidr_block = "0.0.0.0/0"
    from_port  = 1024
    to_port    = 65535
  }
  
  tags = {
    Name = "public-nacl"
  }
}

# VPC Flow Logs
resource "aws_cloudwatch_log_group" "vpc_flow_logs" {
  name = "vpc-flow-logs"
}

resource "aws_iam_role" "vpc_flow_logs" {
  name = "vpc-flow-logs-role"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "vpc-flow-logs.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_flow_log" "vpc" {
  iam_role_arn    = aws_iam_role.vpc_flow_logs.arn
  log_destination = aws_cloudwatch_log_group.vpc_flow_logs.arn
  traffic_type    = "ALL"
  vpc_id         = aws_vpc.main.id
}
```

---

## 8. Checklist de Déploiement Complet

### Phase 1: Planification
- [ ] Définir la stratégie d'adressage IP
- [ ] Choisir les régions et Availability Zones
- [ ] Planifier la segmentation réseau (tiers)
- [ ] Prévoir la croissance future (espace d'adressage)
- [ ] Documenter l'architecture cible

### Phase 2: Déploiement
- [ ] Créer le VPC avec le bloc CIDR principal
- [ ] Créer les sous-réseaux (public/privé/isolé)
- [ ] Déployer l'Internet Gateway
- [ ] Configurer les NAT Gateways (un par AZ)
- [ ] Créer et associer les Route Tables
- [ ] Configurer les NACLs
- [ ] Définir les Security Groups
- [ ] Activer les VPC Flow Logs

### Phase 3: Post-déploiement
- [ ] Tester la connectivité interne
- [ ] Tester la connectivité internet (sortante/entrante)
- [ ] Valider les règles de sécurité
- [ ] Configurer le monitoring et alerting
- [ ] Documenter l'architecture déployée

### Phase 4: Optimisation
- [ ] Implémenter les VPC Endpoints si nécessaire
- [ ] Configurer le VPC Peering si multi-VPC
- [ ] Optimiser les coûts (NAT Gateway sizing)
- [ ] Automatiser via Infrastructure as Code
- [ ] Mettre en place la gestion des changements

---

## Conclusion

Ce cours complet a couvert tous les aspects des VPC AWS, des concepts fondamentaux aux architectures avancées. La maîtrise des VPC est essentielle pour construire des infrastructures cloud sécurisées, performantes et résilientes.

### Points Clés à Retenir :
1. **Planifiez soigneusement** votre adressage IP dès le début
2. **Utilisez le principe de moindre privilège** pour la sécurité
3. **Concevez pour la haute disponibilité** avec multi-AZ
4. **Monitorer continuellement** avec VPC Flow Logs et CloudWatch
5. **Automatisez tout** avec Terraform/CloudFormation
6. **Documentez votre architecture** pour le troubleshooting



# thoereme cap 
 1- disponibilité (availability) (depot 500xaf)
 2- coherance
 3- tolerance au panne (resaux)

disponibilité, coherance, tolerance, faibilite, scalabilite, résilience,

 choisir entre : PC(500) ou PD (facebook) 

