# Cours Complet sur Jenkins

## Table des Matières
1. [Introduction à Jenkins](#introduction)
2. [Architecture de Jenkins](#architecture)
3. [Installation et Configuration](#installation)
4. [Les Jobs/Pipelines](#jobs-pipelines)
5. [Pipeline as Code](#pipeline-as-code)
6. [Intégration avec les Outils DevOps](#integration)
7. [Bonnes Pratiques](#bonnes-pratiques)
8. [Sécurité](#securité)
9. [Monitoring et Maintenance](#monitoring)

---

## 1. Introduction à Jenkins <a name="introduction"></a>

### Qu'est-ce que Jenkins ?
Jenkins est un serveur d'automatisation open source écrit en Java, utilisé pour l'intégration continue (CI) et la livraison continue (CD).

### Concepts Clés
- **Intégration Continue (CI)**: Pratique qui consiste à intégrer fréquemment le code dans un dépôt partagé
- **Livraison Continue (CD)**: Extension de la CI qui automatise le déploiement
- **Build**: Processus de compilation et préparation de l'application
- **Pipeline**: Suite d'étapes automatisées

### Avantages de Jenkins
- Open source et gratuit
- Grande communauté
- Large écosystème de plugins
- Flexible et extensible
- Multiplateforme

---

## 2. Architecture de Jenkins <a name="architecture"></a>

### Composants Principaux
```
┌─────────────────┐    ┌─────────────────┐
│   Master Node   │    │   Agent Node    │
│                 │    │                 │
│ • Orchestration │◄──►│ • Exécution     │
│ • Configuration │    │ • Builds        │
│ • Interface Web │    │ • Tests         │
└─────────────────┘    └─────────────────┘
```

### Master Jenkins
- Gère l'interface utilisateur
- Orchestre les builds
- Stocke la configuration
- Gère les plugins

### Agents/Nœuds
- Exécutent les jobs
- Peuvent être sur différentes plateformes
- Répartissent la charge

---

## 3. Installation et Configuration <a name="installation"></a>

### Installation sur Linux (Ubuntu/Debian)

```bash
# Ajouter le repository Jenkins
wget -q -O - https://pkg.jenkins.io/debian/jenkins.io.key | sudo apt-key add -
sudo sh -c 'echo deb http://pkg.jenkins.io/debian-stable binary/ > /etc/apt/sources.list.d/jenkins.list'

# Mettre à jour et installer
sudo apt update
sudo apt install jenkins

# Démarrer le service
sudo systemctl start jenkins
sudo systemctl enable jenkins
```

### Installation via Docker

```bash
# Créer un réseau Docker
docker network create jenkins

# Lancer Jenkins
docker run \
  --name jenkins-docker \
  --detach \
  --privileged \
  --network jenkins \
  --network-alias docker \
  --env DOCKER_TLS_CERTDIR=/certs \
  --volume jenkins-docker-certs:/certs/client \
  --volume jenkins-data:/var/jenkins_home \
  --publish 8080:8080 \
  --publish 50000:50000 \
  jenkins/jenkins:lts
```

### Configuration Initiale
1. Accéder à `http://localhost:8080`
2. Récupérer le mot de passe initial :
```bash
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```
3. Installer les plugins recommandés
4. Créer un administrateur

### Configuration Système
- **Gestion des Nœuds** : Ajouter des agents
- **Configuration Globale** : Variables d'environnement, outils
- **Gestion des Plugins** : Installation/mise à jour

---

## 4. Les Jobs/Pipelines <a name="jobs-pipelines"></a>

### Types de Jobs

#### 1. Freestyle Project
- Interface graphique simple
- Bon pour des tâches simples
- Configuration via formulaire

#### 2. Pipeline
- Définition en code (Jenkinsfile)
- Plus flexible et maintenable
- Meilleur pour les workflows complexes

#### 3. Multi-branch Pipeline
- Détection automatique des branches
- Pipeline par branche
- Idéal pour Git Flow

### Structure d'un Pipeline

```groovy
pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                // Étapes de build
            }
        }
        stage('Test') {
            steps {
                // Étapes de test
            }
        }
        stage('Deploy') {
            steps {
                // Étapes de déploiement
            }
        }
    }
    post {
        always {
            // Actions post-build
        }
        success {
            // En cas de succès
        }
        failure {
            // En cas d'échec
        }
    }
}
```

---

## 5. Pipeline as Code <a name="pipeline-as-code"></a>

### Syntaxe Déclarative vs Scriptée

#### Syntaxe Déclarative (Recommandée)
```groovy
pipeline {
    agent any
    options {
        timeout(time: 1, unit: 'HOURS')
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }
    environment {
        APP_VERSION = '1.0.0'
        DOCKER_REGISTRY = 'registry.example.com'
    }
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Build') {
            steps {
                sh 'mvn clean compile'
            }
        }
        stage('Unit Tests') {
            steps {
                sh 'mvn test'
            }
            post {
                always {
                    junit 'target/surefire-reports/*.xml'
                }
            }
        }
    }
}
```

#### Syntaxe Scriptée
```groovy
node {
    stage('Checkout') {
        checkout scm
    }
    stage('Build') {
        sh 'mvn clean compile'
    }
    stage('Test') {
        sh 'mvn test'
    }
}
```

### Directives Principales

#### Agent
```groovy
agent {
    docker {
        image 'maven:3.8.1-openjdk-11'
        args '-v $HOME/.m2:/root/.m2'
    }
}
```

#### Environment
```groovy
environment {
    DB_URL = 'jdbc:postgresql://localhost:5432/app'
    CREDENTIALS_ID = 'docker-hub-credentials'
}
```

#### Parameters
```groovy
parameters {
    choice(
        name: 'ENVIRONMENT',
        choices: ['dev', 'staging', 'prod'],
        description: 'Environment to deploy'
    )
    string(
        name: 'VERSION',
        defaultValue: '1.0.0',
        description: 'Application version'
    )
}
```

#### Tools
```groovy
tools {
    maven 'Maven-3.8.1'
    jdk 'OpenJDK-11'
}
```

### Gestion des Échecs et Notifications

```groovy
post {
    always {
        emailext (
            subject: "Build ${currentBuild.result}: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
            body: """
            Build: ${env.BUILD_URL}
            Status: ${currentBuild.result}
            Commit: ${env.GIT_COMMIT}
            """,
            to: 'team@example.com'
        )
    }
    failure {
        slackSend(
            channel: '#builds',
            message: "Build FAILED: ${env.JOB_NAME} #${env.BUILD_NUMBER}"
        )
    }
}
```

---

## 6. Intégration avec les Outils DevOps <a name="integration"></a>

### Intégration Git
```groovy
pipeline {
    agent any
    triggers {
        pollSCM('H/5 * * * *')
    }
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/user/repo.git',
                    credentialsId: 'github-token'
            }
        }
    }
}
```

### Intégration Docker
```groovy
stage('Build Docker Image') {
    steps {
        script {
            docker.build("myapp:${env.BUILD_ID}")
        }
    }
}

stage('Push Docker Image') {
    steps {
        script {
            docker.withRegistry('https://registry.hub.docker.com', 'docker-hub-credentials') {
                docker.image("myapp:${env.BUILD_ID}").push()
            }
        }
    }
}
```

### Intégration Kubernetes
```groovy
stage('Deploy to Kubernetes') {
    steps {
        withKubeConfig([credentialsId: 'k8s-cluster']) {
            sh '''
                kubectl set image deployment/myapp myapp=myapp:${BUILD_ID}
                kubectl rollout status deployment/myapp
            '''
        }
    }
}
```

### Intégration AWS
```groovy
stage('Deploy to AWS') {
    steps {
        withAWS(region: 'us-east-1', credentials: 'aws-credentials') {
            sh 'aws s3 sync dist/ s3://my-bucket/'
        }
    }
}
```

---

## 7. Bonnes Pratiques <a name="bonnes-pratiques"></a>

### Structure des Pipelines

#### 1. Utiliser des Jenkinsfiles
- Stocker le pipeline dans le repository
- Versionner avec le code
- Faciliter les revues de code

#### 2. Pipeline Modularisé
```groovy
// Jenkinsfile principal
@Library('shared-library')_

pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                buildApp()
            }
        }
        stage('Test') {
            steps {
                runTests()
            }
        }
    }
}

// Dans la shared library
// vars/buildApp.groovy
def call() {
    sh 'mvn clean package'
}
```

#### 3. Gestion des Secrets
```groovy
pipeline {
    agent any
    environment {
        DB_PASSWORD = credentials('db-password')
        API_TOKEN = credentials('api-token')
    }
    stages {
        stage('Deploy') {
            steps {
                sh '''
                    echo "Using password: $DB_PASSWORD"
                    deploy --token $API_TOKEN
                '''
            }
        }
    }
}
```

### Optimisation des Performances

#### 1. Utilisation des Agents
```groovy
pipeline {
    agent none
    stages {
        stage('Build') {
            agent {
                label 'linux-docker'
            }
            steps {
                // Build steps
            }
        }
        stage('Test on Windows') {
            agent {
                label 'windows'
            }
            steps {
                // Test steps
            }
        }
    }
}
```

#### 2. Cache et Réutilisation
```groovy
stage('Build') {
    steps {
        sh '''
            # Cache Maven dependencies
            if [ -d "$HOME/.m2" ]; then
                mv $HOME/.m2 /tmp/m2-cache
            fi
            mvn clean compile
        '''
    }
}
```

### Gestion des Branches

#### Pipeline Multi-branches
```groovy
// Jenkinsfile dans chaque branche
pipeline {
    agent any
    when {
        branch 'main'
    }
    stages {
        stage('Deploy to Prod') {
            steps {
                // Déploiement production
            }
        }
    }
}
```

---

## 8. Sécurité <a name="securité"></a>

### Authentification et Autorisation

#### Stratégies d'Authentification
- **Matrix-Based Security** : Contrôle granulaire
- **Project-based Matrix** : Sécurité par projet
- **Role-Based Strategy** : Gestion par rôles

#### Configuration de Sécurité
```groovy
// Dans un script de configuration (Casc)
jenkins:
  securityRealm:
    local:
      allowsSignup: false
      users:
        - id: "admin"
          password: "encrypted_password"
  authorizationStrategy:
    global:
      permissions:
        - "Overall/Administer:admin"
        - "Overall/Read:authenticated"
```

### Gestion des Secrets

#### Utilisation de Credentials
```groovy
withCredentials([
    usernamePassword(
        credentialsId: 'docker-registry',
        usernameVariable: 'DOCKER_USER',
        passwordVariable: 'DOCKER_PASS'
    ),
    string(
        credentialsId: 'api-key',
        variable: 'API_KEY'
    )
]) {
    sh '''
        docker login -u $DOCKER_USER -p $DOCKER_PASS
        curl -H "Authorization: Bearer $API_KEY" https://api.example.com
    '''
}
```

### Sécurité des Pipelines

#### Approbations Manuelles
```groovy
stage('Deploy to Production') {
    steps {
        input message: 'Déployer en production?',
              ok: 'Déployer',
              submitter: 'admin,production-team'
    }
}
```

#### Contrôles d'Accès
```groovy
properties([
    pipelineTriggers([]),
    parameters([
        string(name: 'VERSION', defaultValue: '')
    ]),
    // Restreindre l'exécution aux utilisateurs autorisés
    authorization([
        // Configuration des permissions
    ])
])
```

---

## 9. Monitoring et Maintenance <a name="monitoring"></a>

### Monitoring des Performances

#### Métriques Clés
- Temps d'exécution des builds
- Taux de réussite/échec
- Utilisation des agents
- Temps de réponse de l'interface

#### Scripts de Monitoring
```bash
#!/bin/bash
# Script de monitoring Jenkins

JENKINS_URL="http://localhost:8080"
API_TOKEN="your-api-token"

# Vérifier l'état de Jenkins
curl -s -X GET "${JENKINS_URL}/api/json" \
  --user "admin:${API_TOKEN}" | jq '.'
```

### Sauvegarde et Restauration

#### Configuration de Sauvegarde
```xml
<!-- Configuration plugin ThinBackup -->
<org.jenkinsci.plugins.thinbackup.ThinBackupPlugin plugin="thinbackup@1.0">
  <backupPath>/var/jenkins_backup</backupPath>
  <backupSchedule>0 2 * * *</backupSchedule>
  <backupFilesNo>10</backupFilesNo>
</org.jenkinsci.plugins.thinbackup.ThinBackupPlugin>
```

#### Script de Sauvegarde
```bash
#!/bin/bash
# Sauvegarde Jenkins

JENKINS_HOME="/var/lib/jenkins"
BACKUP_DIR="/backup/jenkins"
DATE=$(date +%Y%m%d_%H%M%S)

tar -czf "${BACKUP_DIR}/jenkins_backup_${DATE}.tar.gz" "$JENKINS_HOME"
find "$BACKUP_DIR" -name "jenkins_backup_*.tar.gz" -mtime +30 -delete
```

### Maintenance Régulière

#### Nettoyage des Workspaces
```groovy
pipeline {
    agent any
    options {
        cleanWs()
    }
    // ...
}
```

#### Gestion des Logs
```groovy
post {
    always {
        archiveArtifacts artifacts: 'target/*.jar', fingerprint: true
        junit 'target/surefire-reports/*.xml'
        // Nettoyage
        cleanWs()
    }
}
```

### Scaling et Haute Disponibilité

#### Configuration Master/Agent
```groovy
// Configuration d'un agent permanent
node('linux-agent-1') {
    stage('Build') {
        // Exécution sur l'agent spécifique
    }
}
```

#### Utilisation d'Agents Cloud
```groovy
pipeline {
    agent {
        kubernetes {
            label 'jenkins-agent'
            yaml """
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: jnlp
    image: jenkins/inbound-agent:4.3-4
    resources:
      limits:
        memory: 512Mi
        cpu: 500m
"""
        }
    }
    stages {
        // Étapes du pipeline
    }
}
```

---

## Conclusion

Jenkins reste un outil essentiel dans l'écosystème DevOps moderne. Sa flexibilité, son extensibilité via les plugins, et sa robustesse en font une solution idéale pour l'automatisation des processus de développement, de test et de déploiement.

### Prochaines Étapes
1. **Pratiquer** avec des projets réels
2. **Explorer les plugins** selon vos besoins
3. **Implémenter la sécurité** dès le début
4. **Automatiser** le maximum de processus
5. **Monitorer** et optimiser continuellement

### Ressources Utiles
- [Documentation Officielle Jenkins](https://www.jenkins.io/doc/)
- [Jenkins Handbook](https://www.jenkins.io/doc/book/)
- [Plugins Jenkins](https://plugins.jenkins.io/)
- [Jenkins Community](https://community.jenkins.io/)

Ce cours couvre les aspects fondamentaux et avancés de Jenkins. La pratique régulière et l'expérimentation sont essentielles pour maîtriser cet outil puissant.