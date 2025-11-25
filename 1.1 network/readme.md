

# En tant qu’ingénieur DevOps / SysAdmin / Linux, tu tapes ces commandes réseau tous les jours. Voici la liste « incontournable », en commençant par ta commande d’origine.

```bash
sudo apt update -y
```
Imagine que ton ordinateur a une grande liste de courses (les paquets qu’on peut installer).  
- `sudo` = « S’il te plaît, fais-le en chef » (parce que seul le chef peut changer la liste de courses)  
- `apt update` = « Va sur Internet et récupère la nouvelle liste de courses mise à jour »  
- `-y` = « Si jamais on te demande “tu es sûr ?”, réponds tout de suite OUI sans attendre »  
→ En vrai, cette commande ne change rien sur l’ordinateur, elle lit juste la nouvelle liste. C’est comme ouvrir le catalogue JouéClub pour voir les nouveaux jouets.

### Les commandes réseau expliquées comme à un enfant

#### 1. « C’est quoi mon adresse et mes prises réseau ? »
```bash
ip a
```
C’est comme demander : « Montre-moi toutes les prises réseau de la maison et les adresses écrites dessus. »  
Tu vois ton Wi-Fi, ta prise Ethernet, ton adresse locale (192.168…).

#### 2. « Par où passe la lettre quand j’envoie quelque chose ? »
```bash
ip r
```
C’est la carte routière de ta maison : « Si je veux parler à Google, je passe par quelle porte ? » (généralement ta box Internet).

#### 3. « Tu m’entends ? » (le plus vieux test du monde)
```bash
ping google.com
```
Tu cries « Y a quelqu’un ? » dans le tuyau Internet et tu attends que Google te réponde « Oui ! ».  
Si ça répond → Internet marche.

#### 4. « Comment on transforme “google.com” en numéro ? »
```bash
dig google.com
```
Les noms comme google.com, c’est pour les humains.  
Les ordinateurs parlent en numéros (comme 142.250.180.78).  
`dig` c’est le traducteur qui change le nom en numéro.

#### 5. « Qui écoute sur quelles portes ? »
```bash
ss -tulnp
```
Imagine ta maison avec plein de portes numérotées (80, 443, 22, 3306…).  
Cette commande te dit :  
« La porte 22 → c’est papa SSH qui attend »  
« La porte 80 → c’est le site web qui écoute »  
Très utile quand un site ne marche pas.

#### 6. « Qui est connecté à la maison en ce moment ? »
```bash
who    ou    w
```
Te dit : « Il y a toi sur le clavier + Paul qui est connecté en SSH depuis son ordi. »

#### 7. « La porte 443 est bien ouverte ? »
```bash
nc -zv google.com 443
```
Tu frappes à la porte 443 de Google.  
Si ça dit “succeeded” → la porte est ouverte → le site https marche.

#### 8. « Ramène-moi ce fichier d’Internet ! »
```bash
curl -O https://example.com/photo.jpg
wget https://example.com/gros-fichier.zip
```
curl et wget = les deux livreurs d’Internet. Tu leur donnes un lien, ils ramènent le fichier à la maison.

#### 9. « C’est quoi la vitesse de ma connexion ? »
```bash
curl -s https://raw.githubusercontent.com/sivel/speedtest-cli/master/speedtest.py | python3 -
```
C’est le test de vitesse comme sur fast.com, mais dans le terminal.

#### 10. « Je veux voir tous les paquets qui passent » (le microscope)
```bash
sudo tcpdump -i any
```
C’est comme mettre une caméra sur le câble réseau : tu vois chaque petite enveloppe qui passe (très utile quand “ça marche pas et on sait pas pourquoi”).

#### 11. Le mur de feu (firewall) – les gardes à l’entrée
Sur Ubuntu (le plus simple) :
```bash
sudo ufw status          → Qui laisse passer qui ?
sudo ufw allow 22         → Laisse passer SSH (sinon tu te bloques dehors !)
sudo ufw allow 80         → Laisse passer les sites web
sudo ufw deny 23          → Interdit l’ancien telnet (dangereux)
```

#### 12. « Comment s’appelle mon ordi ? »
```bash
hostnamectl set-hostname lapin-magique
```
Tu donnes un petit nom mignon à ton serveur (au lieu de ubuntu-1234).

#### 13. Lever ou baisser une prise réseau
```bash
sudo ip link set eth0 down    → Je débranche le câble (virtuellement)
sudo ip link set eth0 up      → Je rebranche
```

### La commande magique que tout le monde garde dans ses favoris
```bash
ip a ; ip r ; ss -tulnp ; ping -c1 8.8.8.8 ; curl ifconfig.me
```
En une seule ligne tu sais :
- Mes adresses IP
- Ma route Internet
- Ce qui écoute
- Si Internet marche
- Mon IP publique

C’est comme le “check-up” complet de ta machine en 2 secondes.

Garde cette page dans tes favoris ou fais-toi une petite antisèche plastifiée.  
Dans 2 semaines tu connaîtras tout ça par cœur et tu feras peur à tes collègues avec ta vitesse au terminal ! 😄
