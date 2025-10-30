# Jenkins – De Zéro à Héros

Souhaitez-vous apprendre **Jenkins** depuis les bases (installation) jusqu’à un niveau avancé (création de pipelines CI/CD de bout en bout) ?
Alors vous êtes au bon endroit.

---

## Installation sur une instance EC2

![Screenshot 2023-02-01 at 5 46 14 PM](https://user-images.githubusercontent.com/43399466/216040281-6c8b89c3-8c22-4620-ad1c-8edd78eb31ae.png)

Installez Jenkins, configurez Docker comme agent, mettez en place un pipeline CI/CD, déployez des applications sur Kubernetes, et bien plus encore.

---

## Instance AWS EC2

* Rendez-vous sur la **console AWS**
* Ouvrez **Instances (running)**
* Cliquez sur **Launch instances**

<img width="994" alt="Screenshot 2023-02-01 at 12 37 45 PM" src="https://user-images.githubusercontent.com/43399466/215974891-196abfe9-ace0-407b-abd2-adcffe218e3f.png">

---

### Installation de Jenkins

**Prérequis :**

* Java (JDK)

### Exécutez les commandes suivantes pour installer Java et Jenkins

**Installer Java :**

```bash
sudo apt update
sudo apt install openjdk-17-jre
```

**Vérifier l’installation de Java :**

```bash
java -version
```

Vous pouvez maintenant procéder à l’installation de Jenkins :

```bash
curl -fsSL https://pkg.jenkins.io/debian/jenkins.io-2023.key | sudo tee \
  /usr/share/keyrings/jenkins-keyring.asc > /dev/null
echo deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] \
  https://pkg.jenkins.io/debian binary/ | sudo tee \
  /etc/apt/sources.list.d/jenkins.list > /dev/null
sudo apt-get update
sudo apt-get install jenkins
```

---

**Remarque :**
Par défaut, Jenkins n’est pas accessible depuis l’extérieur à cause des restrictions de trafic entrant imposées par AWS.
Ouvrez le **port 8080** dans les règles de trafic entrant comme indiqué ci-dessous :

* EC2 > Instances > Cliquez sur votre **Instance-ID**
* Dans les onglets en bas → **Security**
* **Security groups**
* Ajoutez une règle de trafic entrant (vous pouvez autoriser uniquement le **TCP 8080**, ou bien « All traffic » comme dans l’exemple ci-dessous).

<img width="1187" alt="Screenshot 2023-02-01 at 12 42 01 PM" src="https://user-images.githubusercontent.com/43399466/215975712-2fc569cb-9d76-49b4-9345-d8b62187aa22.png">

---

### Connexion à Jenkins

Accédez à l’URL suivante :
**http://<adresse-IP-publique-ec2>:8080**

(L’adresse IP publique est disponible sur la console AWS EC2.)

**Remarque :**
Si vous ne souhaitez pas autoriser tout le trafic :

1. Supprimez la règle de trafic entrant existante.
2. Créez une nouvelle règle pour autoriser uniquement le port **8080 (TCP)**.

---

Après connexion à Jenkins :

* Exécutez la commande suivante pour récupérer le mot de passe administrateur :

  ```bash
  sudo cat /var/lib/jenkins/secrets/initialAdminPassword
  ```
* Entrez ce mot de passe dans l’interface d’administration.

<img width="1291" alt="Screenshot 2023-02-01 at 10 56 25 AM" src="https://user-images.githubusercontent.com/43399466/215959008-3ebca431-1f14-4d81-9f12-6bb232bfbee3.png">

---

### Cliquez sur **Install suggested plugins**

<img width="1291" alt="Screenshot 2023-02-01 at 10 58 40 AM" src="https://user-images.githubusercontent.com/43399466/215959294-047eadef-7e64-4795-bd3b-b1efb0375988.png">

Attendez que Jenkins installe les plugins recommandés.

<img width="1291" alt="Screenshot 2023-02-01 at 10 59 31 AM" src="https://user-images.githubusercontent.com/43399466/215959398-344b5721-28ec-47a5-8908-b698e435608d.png">

Créez le premier utilisateur administrateur (recommandé si vous souhaitez utiliser cette instance Jenkins pour d’autres projets futurs), ou passez cette étape.

<img width="990" alt="Screenshot 2023-02-01 at 11 02 09 AM" src="https://user-images.githubusercontent.com/43399466/215959757-403246c8-e739-4103-9265-6bdab418013e.png">

**L’installation de Jenkins est terminée avec succès !**
Vous pouvez maintenant commencer à l’utiliser.

<img width="990" alt="Screenshot 2023-02-01 at 11 14 13 AM" src="https://user-images.githubusercontent.com/43399466/215961440-3f13f82b-61a2-4117-88bc-0da265a67fa7.png">

---

## Installation du plugin Docker Pipeline dans Jenkins

1. Connectez-vous à Jenkins.
2. Allez dans **Manage Jenkins > Manage Plugins**.
3. Sous l’onglet **Available**, recherchez **Docker Pipeline**.
4. Sélectionnez le plugin et cliquez sur **Install**.
5. Redémarrez Jenkins après l’installation.

<img width="1392" alt="Screenshot 2023-02-01 at 12 17 02 PM" src="https://user-images.githubusercontent.com/43399466/215973898-7c366525-15db-4876-bd71-49522ecb267d.png">

Attendez que Jenkins redémarre.

---

## Configuration d’un agent Docker (Docker Slave)

Exécutez les commandes suivantes pour installer Docker :

```bash
sudo apt update
sudo apt install docker.io
```

### Donner les permissions nécessaires à Jenkins et à l’utilisateur Ubuntu pour accéder au démon Docker

```bash
sudo su - 
usermod -aG docker jenkins
usermod -aG docker ubuntu
systemctl restart docker
```

Une fois ces étapes terminées, il est recommandé de redémarrer Jenkins :

```
http://<adresse-IP-publique-ec2>:8080/restart
```

✅ **La configuration de l’agent Docker est maintenant réussie.**
