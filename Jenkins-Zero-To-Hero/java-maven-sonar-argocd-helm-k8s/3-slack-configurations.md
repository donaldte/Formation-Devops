# 🚀 **Intégration Slack + Jenkins : Guide Complet**

L’objectif est de permettre à Jenkins d’envoyer automatiquement des notifications Slack à chaque :

* ✔️ Succès du pipeline
* ❌ Échec du pipeline

Grâce au **plugin officiel Slack Notification**.

---

# 📌 **1. Préparer l’intégration Slack**

### 1.1. Ajouter l’application Slack "Jenkins CI"

1. Ouvrir Slack
2. Aller dans : **marketplace app**
3. Rechercher : **Jenkins CI**
4. Cliquer sur **Add to Slack**
5. Choisir le channel (ex : `#general`)
6. Slack génère un **Integration Token** comme :

```
2E8IFdh6pX0VJlRC32xri5LS
```

👉 **Ce token sert à connecter Jenkins à Slack.**

---

# 📌 **2. Ajouter le token Slack dans Jenkins (Credentials)**

Dans Jenkins :

1. Aller à :
   **Manage Jenkins → Credentials → System → Global credentials → Add Credentials**
2. Remplir :

| Champ      | Valeur              |
| ---------- | ------------------- |
| **Kind**   | Secret text         |
| **Secret** | `<TON_TOKEN_SLACK>` |
| **ID**     | `slack-token`       |

👉 Exemple de secret :

```
2E8IFdh6pX0VJlRC32xri5LS
```

---

# 📌 **3. Configurer Slack au niveau global dans Jenkins**

1. Aller dans :
   **Manage Jenkins → Configure System**
2. Trouver la section :
   **Global Slack Notifier Settings**

Remplir :

| Champ                               | Valeur                                                     |
| ----------------------------------- | ---------------------------------------------------------- |
| **Team Subdomain**                  | `hooyia`                                                   |
| **Integration Token Credential ID** | `slack-token`                                              |
| **Default Channel**                 | `#general` (ou laisse vide pour préciser dans Jenkinsfile) |

3. Cliquer **Save**

Ceci connecte entièrement Jenkins ↔ Slack.

---

# 📌 **4. Ajouter les notifications Slack dans ton Jenkinsfile**

Tu peux maintenant utiliser `slackSend`, fourni par le plugin.

### 4.1. Ajouter la section post-build

À la fin du Jenkinsfile, ajoute :

```groovy
post {

  success {
    slackSend(
      channel: '#general',
      color: '#36a64f',
      message: "🎉 SUCCESS — Build *#${BUILD_NUMBER}* déployé avec succès ! 🚀"
    )
  }

  failure {
    slackSend(
      channel: '#general',
      color: '#ff0000',
      message: "❌ FAILURE — Le pipeline a échoué au build *#${BUILD_NUMBER}*. ⚠️"
    )
  }

}
```

### Explication :

| État        | Notification              |
| ----------- | ------------------------- |
| **success** | envoie un message vert 🎉 |
| **failure** | envoie un message rouge ❌ |

---

# 📌 **5. Exemple complet de Jenkinsfile avec Slack**

Voici la partie **Slack uniquement** :

```groovy
post {

  success {
    slackSend(
      channel: '#general',
      color: '#36a64f',
      message: "🎉 SUCCESS — Build *#${BUILD_NUMBER}* déployé avec succès ! 🚀"
    )
  }

  failure {
    slackSend(
      channel: '#general',
      color: '#ff0000',
      message: "❌ FAILURE — Le pipeline a échoué au build *#${BUILD_NUMBER}*. ⚠️"
    )
  }

}
```

---

# 📌 **6. Vérification du bon fonctionnement**

À chaque build :

### ✔️ En cas de succès

Slack reçoit :

```
🎉 SUCCESS — Build #12 déployé avec succès ! 🚀
```

### ❌ En cas d'échec

Slack reçoit :

```
❌ FAILURE — Le pipeline a échoué au build #12. ⚠️
```

---

# 📌 **7. (Optionnel) Tester la configuration Slack**

Dans Jenkins :

```
Manage Jenkins → Configure System → Slack → Test Connection
```

Tu devrais voir dans Slack :

```
Jenkins CI integration successful!
```

---

# 📌 **8. Résumé Final**

| Étape                                         | Description                             |
| --------------------------------------------- | --------------------------------------- |
| 1. Ajouter l’app Jenkins CI dans Slack        | Génère un Token                         |
| 2. Ajouter le token dans Jenkins              | Credentials → Secret text               |
| 3. Configurer Slack dans Jenkins              | Team subdomain + Token                  |
| 4. Ajouter les notifications dans Jenkinsfile | success / failure                       |
| 5. Tester                                     | Build Jenkins → Slack envoie un message |

---

