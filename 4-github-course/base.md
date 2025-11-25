
# 🚀 Cours Professionnel : Git & GitHub Actions pour DevOps Engineers

## 🎯 Objectif du cours
Maîtriser Git et GitHub Actions pour construire un pipeline CI/CD robuste, sécurisé et automatisé, basé sur une application Flask. Ce cours couvre :
- **Gestion professionnelle de Git** : commits, branches, tags et releases.
- **Pipeline CI/CD** : tests automatisés, linting, audits de sécurité, notifications d’échec.
- **Bonnes pratiques DevOps** : conventions de nommage, gestion des secrets, versionnement sémantique.
- **Explications claires** : chaque commande et fichier est expliqué pour une compréhension approfondie.

---

## 📦 Application Exemple : API Flask Minimale
Nous utilisons une application Flask simple pour illustrer les concepts. Voici la structure du projet :

```
flaskapp/
├── app.py                # Point d'entrée de l'application Flask
├── requirements.txt      # Dépendances Python
├── tests/
│   └── test_app.py       # Tests unitaires avec pytest
├── .gitignore            # Fichiers à ignorer par Git
└── .github/
    └── workflows/
        └── ci.yml        # Configuration du pipeline CI/CD
```

### 📄 Fichier `app.py`
```python
from flask import Flask, jsonify

# Créer une instance de l'application Flask
app = Flask(__name__)

# Route simple pour tester l'API
@app.route("/hello", methods=["GET"])
def hello():
    return jsonify({"message": "Hello from Flask!"})

# Point d'entrée pour lancer l'application
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
```

**Explication** :
- `Flask(__name__)` : Initialise une application Flask.
- `@app.route("/hello")` : Définit une route GET `/hello` qui retourne un JSON.
- `debug=True` : Utilisé uniquement en développement local (désactivé en production pour des raisons de sécurité).

### 📄 Fichier `requirements.txt`
```
Flask==2.3.2
pytest==7.2.0
```

**Explication** :
- Liste les dépendances nécessaires pour l’application et les tests.
- Les versions spécifiques (`==`) garantissent la reproductibilité des environnements.

### 📄 Fichier `tests/test_app.py`
```python
from app import app

def test_hello():
    client = app.test_client()  # Simule un client HTTP
    response = client.get("/hello")  # Envoie une requête GET
    assert response.status_code == 200  # Vérifie le code HTTP
    assert response.json == {"message": "Hello from Flask!"}  # Vérifie la réponse
```

**Explication** :
- Utilise `pytest` pour tester la route `/hello`.
- Vérifie que la réponse HTTP est correcte (code 200) et que le JSON retourné est conforme.

### 📄 Fichier `.gitignore`
```
__pycache__/
*.pyc
venv/
.env
```

**Explication** :
- Ignore les fichiers temporaires Python (bytecode, dossiers de cache).
- Ignore les environnements virtuels (`venv/`) et les fichiers de configuration sensibles (`.env`).

---

## 🧱 Étape 1 : Initialisation Git Professionnelle

### Commandes
```bash
# Initialiser un dépôt Git
git init

# Créer un fichier .gitignore
echo '__pycache__/\n*.pyc\nvenv/\n.env' > .gitignore

# Ajouter tous les fichiers
git add .

# Créer un commit initial avec un message clair
git commit -m "feat: initialisation application Flask avec route /hello"
```

### Explications
- `git init` : Crée un dépôt Git local vide.
- `.gitignore` : Évite de versionner des fichiers inutiles ou sensibles (ex. : fichiers compilés, environnements virtuels).
- `git add .` : Ajoute tous les fichiers non ignorés au suivi Git.
- `git commit -m "feat: ..."` : Utilise une convention de message de commit (inspirée de **Conventional Commits**) pour un historique clair :
  - `feat` : Nouvelle fonctionnalité.
  - Message descriptif pour faciliter la traçabilité et l’automatisation CI/CD.

### Pourquoi c’est important ?
- Un historique Git propre facilite la collaboration, le débogage et l’intégration avec des outils CI/CD.
- Les conventions de commit permettent d’automatiser la génération de changelogs ou de déclencher des workflows spécifiques.

---

## 🌿 Étape 2 : Gestion des Branches (Stratégie DevOps)

### Commandes
```bash
# Créer et basculer sur une branche pour les tests
git checkout -b test/unit-tests

# Ajouter un test et valider
git add tests/test_app.py
git commit -m "test: ajout du test unitaire pour la route /hello"

# Revenir à la branche main et fusionner
git checkout main
git merge test/unit-tests

# Supprimer la branche une fois fusionnée
git branch -d test/unit-tests
```

### Convention de nommage des branches
Adoptez une stratégie de branching structurée pour CI/CD :
- `main` : Code stable, prêt pour la production.
- `develop` : Code en cours de validation, pour l’intégration continue.
- `feature/xyz` : Développement de nouvelles fonctionnalités (ex. : `feature/add-user-route`).
- `test/xyz` : Tests expérimentaux ou unitaires (ex. : `test/api-endpoints`).
- `hotfix/xyz` : Correctifs urgents pour la production (ex. : `hotfix/fix-login-bug`).

### Explications
- `git checkout -b test/unit-tests` : Crée et bascule sur une nouvelle branche pour isoler les changements.
- `git merge` : Intègre les modifications de la branche `test/unit-tests` dans `main`.
- **Pourquoi isoler les changements ?** Cela permet de tester les modifications sans affecter le code stable et facilite la revue de code via des Pull Requests (PR).
- **Pourquoi supprimer la branche ?** Une fois fusionnée, la branche n’est plus nécessaire, ce qui maintient le dépôt propre.

### Bonnes pratiques
- Toujours travailler sur des branches spécifiques pour éviter de modifier directement `main` ou `develop`.
- Utiliser des PR pour valider les changements avant fusion (revue par les pairs, tests automatisés).
- Adopter une convention de nommage claire pour automatiser les déclencheurs CI/CD.

---

## ⚙️ Étape 3 : Pipeline CI avec GitHub Actions

### 📄 Fichier `.github/workflows/ci.yml`
```yaml
name: Flask CI Pipeline

# Déclencheurs : push ou PR sur main/develop
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - name: 🧾 Cloner le dépôt
      uses: actions/checkout@v4

    - name: 🐍 Configurer Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.10'

    - name: 📦 Installer les dépendances
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt

    - name: ✅ Exécuter les tests unitaires
      run: pytest tests/ --verbose

    - name: 🛡️ Audit de sécurité des dépendances
      run: |
        pip install pip-audit
        pip-audit
```

### Explications
- **Déclencheurs (`on`)** :
  - Le pipeline s’exécute sur tout `push` ou `pull_request` vers `main` ou `develop`.
  - Cela garantit que tout code poussé est testé automatiquement.
- **Job `build`** :
  - `runs-on: ubuntu-latest` : Exécute le pipeline sur une machine virtuelle Ubuntu.
  - `actions/checkout@v4` : Clone le dépôt dans l’environnement du pipeline.
  - `actions/setup-python@v5` : Configure Python 3.10.
  - Installation des dépendances via `requirements.txt`.
  - Exécution des tests avec `pytest`.
  - Audit de sécurité avec `pip-audit` pour détecter les vulnérabilités dans les dépendances.

### Pourquoi c’est important ?
- **Tests automatisés** : Garantissent que le code est fonctionnel avant d’être fusionné.
- **Audit de sécurité** : Identifie les dépendances vulnérables pour réduire les risques en production.
- **Reproductibilité** : L’utilisation de versions spécifiques (Python, dépendances) assure des builds cohérents.

---

## 🚨 Étape 4 : Notifications d’Échec par Email

### Mise à jour du fichier `ci.yml`
Ajoutez un job pour envoyer une alerte en cas d’échec :
```yaml
  notify:
    needs: build  # S'exécute après le job build
    if: failure()  # S'exécute uniquement si le build échoue
    runs-on: ubuntu-latest
    steps:
      - name: 🚨 Envoyer une alerte email
        uses: dawidd6/action-send-mail@v3
        with:
          server_address: smtp.gmail.com
          server_port: 465
          username: ${{ secrets.MAIL_USER }}
          password: ${{ secrets.MAIL_PASS }}
          to: devops@monapp.io
          subject: "🚨 Échec du pipeline CI pour FlaskApp"
          body: |
            ❌ Échec du pipeline CI !
            👉 Repo : ${{ github.repository }}
            👉 Branche : ${{ github.ref }}
            👉 Commit : ${{ github.sha }}
            Consultez les logs pour plus de détails : ${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}
```

### Configuration des secrets
1. Allez dans **Settings → Secrets and variables → Actions** sur GitHub.
2. Ajoutez deux secrets :
   - `MAIL_USER` : Votre adresse email (ex. : `devops@gmail.com`).
   - `MAIL_PASS` : Mot de passe ou jeton d’application SMTP (pour Gmail, utilisez un mot de passe d’application).

### Explications
- **Condition `if: failure()`** : Le job `notify` s’exécute uniquement si le job `build` échoue.
- **Action `dawidd6/action-send-mail@v3`** : Envoie un email via SMTP.
- **Secrets** : Les identifiants SMTP sont stockés de manière sécurisée dans GitHub Secrets, jamais en clair dans le code.
- **Contenu de l’email** : Fournit des informations utiles (repo, branche, commit, lien vers les logs) pour diagnostiquer l’échec rapidement.

### Pourquoi c’est important ?
- Les alertes immédiates permettent aux DevOps de réagir rapidement aux échecs avant qu’ils n’impactent la production.
- Les secrets sécurisés protègent les informations sensibles.

---

## 🏷️ Étape 5 : Tags et Releases pour un Déploiement Contrôlé

### Création d’un Tag
```bash
# Créer un tag sémantique
git tag -a v1.0.0 -m "Release stable v1.0.0"

# Pousser le tag vers GitHub
git push origin v1.0.0
```

### Mise à jour du fichier `ci.yml` pour les releases
Ajoutez un job pour créer une release automatique sur les tags :
```yaml
  release:
    if: startsWith(github.ref, 'refs/tags/v')  # S'exécute uniquement sur les tags commençant par 'v'
    runs-on: ubuntu-latest
    needs: build  # S'exécute après le job build
    steps:
      - name: 🧾 Cloner le dépôt
        uses: actions/checkout@v4

      - name: 📦 Créer une release GitHub
        uses: softprops/action-gh-release@v1
        with:
          tag_name: ${{ github.ref_name }}
          name: Release ${{ github.ref_name }}
          body: |
            Release stable de l'application Flask.
            - Route /hello fonctionnelle
            - Tests unitaires validés
            - Audit de sécurité effectué
          draft: false
          prerelease: false
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### Explications
- **Tag sémantique** (`v1.0.0`) : Suit la convention de versionnement sémantique (`MAJEUR.MINEUR.CORRECTIF`).
- `git tag -a` : Crée un tag annoté avec un message descriptif.
- **Job `release`** :
  - Déclenché uniquement sur les tags commençant par `v` (ex. : `v1.0.0`).
  - Utilise `softprops/action-gh-release@v1` pour créer une release GitHub.
  - La release inclut un changelog clair pour documenter les changements.
- **Secrets** : `GITHUB_TOKEN` est automatiquement fourni par GitHub pour authentifier les actions.

### Pourquoi c’est important ?
- Les **tags** marquent des versions stables dans l’historique Git, facilitant les retours en arrière ou les déploiements.
- Les **releases** fournissent une version packagée (avec changelog) pour les équipes QA, marketing ou clients.
- L’automatisation des releases réduit les erreurs manuelles et améliore la traçabilité.

---

## ✅ Résultat Final
- Une application Flask testée automatiquement à chaque push ou PR.
- Un pipeline CI/CD qui inclut :
  - Tests unitaires (`pytest`).
  - Audit de sécurité (`pip-audit`).
  - Notifications par email en cas d’échec.
- Une gestion des branches structurée pour isoler les environnements (dev, prod).
- Des tags et releases pour marquer les versions stables et faciliter les déploiements.
- Des pratiques sécurisées (secrets, .gitignore) pour protéger le code et les identifiants.

---

## 🔍 Bonnes Pratiques DevOps à Retenir
1. **Commits clairs** : Utilisez des messages structurés (ex. : `feat:`, `fix:`, `test:`) pour un historique lisible.
2. **Branches dédiées** : Isolez les fonctionnalités, tests et correctifs pour maintenir un code stable.
3. **Tests automatisés** : Intégrez des tests unitaires et des audits de sécurité dans le pipeline CI/CD.
4. **Notifications** : Configurez des alertes pour une réactivité immédiate en cas d’échec.
5. **Versionnement sémantique** : Utilisez des tags (`vX.Y.Z`) pour marquer les versions stables.
6. **Sécurité** : Stockez les secrets dans GitHub Secrets, jamais dans le code.
7. **Documentation** : Maintenez un changelog clair dans les releases pour les autres équipes.

---

## 🛠️ Étapes Suivantes (Optionnel)
- Ajouter un déploiement automatisé vers un serveur (ex. : AWS, Heroku, Docker).
- Intégrer un linter (ex. : `flake8`) pour vérifier la qualité du code.
- Configurer des tests d’intégration ou des tests de charge.
- Ajouter des métriques de performance dans le pipeline (ex. : temps d’exécution des tests).

