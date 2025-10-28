# CIDR (Classless Inter-Domain Routing) - Explication Complète

## 🎯 Définition du CIDR

**CIDR** (Classless Inter-Domain Routing) est une méthode d'allocation d'adresses IP et de routage internet qui remplace l'ancien système basé sur les classes (Class A, B, C).

## 📊 Comparaison Ancien vs Nouveau Système

### Système avec Classes (Ancien)
```
Classe A: 0.0.0.0 - 127.255.255.255   /8
Classe B: 128.0.0.0 - 191.255.255.255 /16  
Classe C: 192.0.0.0 - 223.255.255.255 /24
```

### Système CIDR (Moderne)
```
Plage flexible: 10.0.0.0/8 à 10.0.0.0/32
```

## 🔢 Notation CIDR - Explication Visuelle

### Structure d'une Adresse IP
```
Adresse IP: 192.168.1.150
Binaire:    11000000.10101000.00000001.10010110

Masque:     /24 (255.255.255.0)
Binaire:    11111111.11111111.11111111.00000000
            ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑
            24 bits réseau + 8 bits hôtes
```

### Table des Masques CIDR Courants
```
┌──────────┬─────────────────┬─────────────┬─────────────────────┐
│ CIDR     │ Masque          │ Adresses IP │ Exemple de Plage    │
├──────────┼─────────────────┼─────────────┼─────────────────────┤
│ /8       │ 255.0.0.0       │ 16,777,216  │ 10.0.0.0 - 10.255.255.255 │
│ /16      │ 255.255.0.0     │ 65,536      │ 10.0.0.0 - 10.0.255.255   │
│ /20      │ 255.255.240.0   │ 4,096       │ 10.0.0.0 - 10.0.15.255    │
│ /24      │ 255.255.255.0   │ 256         │ 10.0.1.0 - 10.0.1.255     │
│ /26      │ 255.255.255.192 │ 64          │ 10.0.1.0 - 10.0.1.63      │
│ /28      │ 255.255.255.240 │ 16          │ 10.0.1.0 - 10.0.1.15      │
│ /32      │ 255.255.255.255 │ 1           │ 10.0.1.50 - 10.0.1.50     │
└──────────┴─────────────────┴─────────────┴─────────────────────┘
```

## 🧮 Calcul du Nombre d'Adresses

### Formule Mathématique
```
Nombre d'adresses = 2^(32 - préfixe)

Exemples:
/16 : 2^(32-16) = 2^16 = 65,536 adresses
/24 : 2^(32-24) = 2^8 = 256 adresses
/28 : 2^(32-28) = 2^4 = 16 adresses
```

### Adresses Utilisables dans AWS
```
Dans AWS, 5 adresses sont réservées par sous-réseau:

Adresses utilisables = 2^(32 - préfixe) - 5

Exemple pour /24:
256 - 5 = 251 adresses utilisables
```

## 🔍 Détail des Adresses Réservées AWS

```
Sous-réseau: 10.0.1.0/24 (256 adresses totales)

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

## 📐 Comment Calculer une Plage CIDR

### Exemple 1: 10.0.0.0/16
```
Adresse réseau: 10.0.0.0
Masque: 255.255.0.0
Plage: 10.0.0.0 - 10.0.255.255
Adresses: 65,536
Utilisables: 65,531 (en AWS)
```

### Exemple 2: 192.168.1.0/26
```
Adresse réseau: 192.168.1.0
Masque: 255.255.255.192
Plage: 192.168.1.0 - 192.168.1.63
Adresses: 64
Utilisables: 59 (en AWS)
```

## 🎨 Visualisation des Blocs CIDR

### Division d'un VPC /16 en Sous-réseaux
```
VPC: 10.0.0.0/16 (65,536 adresses)

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

## 🛠️ Calcul Manuel d'une Plage CIDR

### Étape par Étape pour 172.16.100.0/22

**1. Déterminer le masque:**
```
/22 = 255.255.252.0
```

**2. Convertir en binaire:**
```
Adresse: 172.16.100.0
Binaire: 10101100.00010000.01100100.00000000

Masque:  11111111.11111111.11111100.00000000
```

**3. Identifier la partie réseau:**
```
Les 22 premiers bits sont fixes:
10101100.00010000.011001 - partie réseau (22 bits)
```

**4. Calculer la plage:**
```
Adresse réseau:   172.16.100.0
Première IP:      172.16.100.1  
Dernière IP:      172.16.103.254
Adresse broadcast:172.16.103.255
```

## 📈 Table de Référence CIDR Complète

```
┌──────────┬─────────────┬──────────┬────────────┬─────────────────────┐
│ Préfixe │ Masque      │ Bloc Size│ Sous-réseaux│ Plage Hôtes         │
├──────────┼─────────────┼──────────┼────────────┼─────────────────────┤
│ /20      │ 255.255.240.0│ 4,096    │ 16 x /24   │ .0 - .15.255        │
│ /21      │ 255.255.248.0│ 2,048    │ 8 x /24    │ .0 - .7.255         │
│ /22      │ 255.255.252.0│ 1,024    │ 4 x /24    │ .0 - .3.255         │
│ /23      │ 255.255.254.0│ 512      │ 2 x /24    │ .0 - .1.255         │
│ /24      │ 255.255.255.0│ 256      │ 1 x /24    │ .0 - .255           │
│ /25      │ 255.255.255.128│ 128     │ 2 x /26    │ .0 - .127           │
│ /26      │ 255.255.255.192│ 64      │ 4 x /28    │ .0 - .63            │
│ /27      │ 255.255.255.224│ 32      │ 8 x /30    │ .0 - .31            │
│ /28      │ 255.255.255.240│ 16      │ 16 x /32   │ .0 - .15            │
└──────────┴─────────────┴──────────┴────────────┴─────────────────────┘
```

## 💡 Bonnes Pratiques CIDR pour AWS

### 1. Taille Recommandée pour VPC
```
✅ RECOMMANDÉ: /16 (65,536 IPs)
🟡 ACCEPTABLE:  /20 (4,096 IPs)  
❌ ÉVITER:      /28 ou plus petit (trop petit)
```

### 2. Planification de la Croissance
```
VPC: 10.0.0.0/16

Répartition recommandée:
• Web:     10.0.0.0/19     (8,192 IPs)
• App:     10.0.32.0/19    (8,192 IPs) 
• Data:    10.0.64.0/19    (8,192 IPs)
• Réservé: 10.0.96.0/19    (8,192 IPs)
```

### 3. Éviter les Chevauchements
```
❌ MAUVAIS:
VPC A: 10.0.0.0/16
VPC B: 10.0.1.0/24  ← Chevauchement!

✅ BON:
VPC A: 10.0.0.0/16
VPC B: 10.1.0.0/16  ← Pas de chevauchement
```

## 🔧 Outils de Calcul CIDR

### Commandes Utiles
```bash
# Calculer la plage d'un CIDR
ipcalc 10.0.0.0/16

# Vérifier si une IP est dans un CIDR
ipcalc 10.0.1.50/24

# Sous-diviser un CIDR
ipcalc 10.0.0.0/16 --s 24
```

### Sites Web Utiles
- **ipaddressguide.com/cidr**
- **cidr.xyz** 
- **subnet-calculator.com**

## 🎓 Résumé des Points Clés

1. **CIDR = Flexibilité** - Plus flexible que le système par classes
2. **Notation IP/Préfixe** - Ex: 192.168.1.0/24
3. **Calcul: 2^(32-préfixe)** - Pour le nombre d'adresses
4. **AWS réserve 5 IPs** - Par sous-réseau
5. **/16 recommandé** - Pour les VPC AWS
6. **Planifier large** - Prévoir la croissance future

Le CIDR est fondamental pour bien concevoir vos réseaux AWS et éviter les problèmes d'adressage IP! 🚀