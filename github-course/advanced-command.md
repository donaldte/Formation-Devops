# 🚀 Cours Professionnel : Commandes Git Avancées pour DevOps Engineers

## 🎯 Objectif du cours
Ce cours est exclusivement dédié aux DevOps Engineers et se concentre sur les commandes Git avancées. Il couvre les stratégies de gestion des branches avancées (comme `staging`, `pre-prod`, `post-merge` ou équivalents), les tags, et d'autres commandes professionnelles pour optimiser les pipelines CI/CD, la collaboration en équipe, et la gestion des environnements (dev, staging, prod). 

Nous n'aborderons pas les bases (comme `git init` ou `git add`) ; le focus est sur les commandes avancées. Chaque commande est expliquée en détail, avec son utilisation en contexte DevOps, des exemples concrets (basés sur l'application Flask des cours précédents), des pièges courants, et des intégrations CI/CD (ex. : GitHub Actions).

**Prérequis** : Maîtrise des bases Git et des stratégies de branching (GitFlow, GitHub Flow). Nous supposons un dépôt distant sur GitHub.

---

## 🔍 Noms des Branches et Éléments Avancés Courants en DevOps
Avant de plonger dans les commandes, voici une liste claire des noms de branches et éléments mentionnés (staging, pre-, post-, tags, etc.) adaptés à un workflow DevOps. Ces noms ne sont pas standards Git, mais des conventions professionnelles pour mapper les branches aux environnements CI/CD :

- **staging** : Branche pour l'environnement de staging (tests finaux avant prod). Code validé mais non déployé en production.
- **pre-prod** (ou `pre-production`) : Branche pour des tests pré-production (ex. : simulations de charge, audits de sécurité). Souvent une copie de `staging` avec des configs spécifiques.
- **post-merge** (ou `post-integration`) : Branche temporaire post-fusion pour des validations automatisées (ex. : tests d'intégration après merge).
- **release/xyz** : Branches pour préparer les releases (ex. : `release/v1.2.0`), incluant des ajustements finaux.
- **hotfix/xyz** : Correctifs urgents directement sur prod.
- **feature/xyz** : Nouvelles fonctionnalités.
- **bugfix/xyz** : Corrections de bugs.
- **Tags** : Points fixes dans l'historique (ex. : `v1.0.0`), utilisés pour déclencher des déploiements ou marquer des versions stables.
- **Hooks** (pré- et post-) : Scripts automatisés (ex. : `pre-commit`, `post-merge`) pour valider le code avant/après des actions Git.

Ces conventions facilitent l'automatisation : par exemple, un push sur `staging` déclenche des tests QA, tandis qu'un tag déclenche un déploiement.

---

## ⚙️ Commandes Avancées pour la Gestion des Branches

### 1. **git branch --merged / --no-merged** (Audit des Branches)
   - **Description** : Liste les branches mergées (ou non) dans la branche actuelle. Utile pour nettoyer le dépôt en DevOps, évitant l'accumulation de branches obsolètes qui polluent les pipelines CI/CD.
   - **Exemple** :
     ```bash
     git checkout main
     git branch --merged  # Liste les branches déjà mergées dans main (ex. : staging si fusionnée)
     git branch --no-merged  # Liste les branches non mergées (ex. : pre-prod)
     ```
   - **Explication DevOps** : Avant un nettoyage automatisé, utilisez ceci pour identifier les branches à supprimer. Intégrez dans un script CI/CD pour un "branch cleanup" hebdomadaire.
   - **Pièges** : Toujours fetch d'abord (`git fetch --prune`) pour synchroniser les branches distantes supprimées.
   - **Intégration CI/CD** : Dans GitHub Actions, ajoutez un job pour lister et supprimer automatiquement les branches mergées via API GitHub.

### 2. **git checkout -b <branche> <commit>** (Création depuis un Commit Spécifique)
   - **Description** : Crée une branche à partir d'un commit ou tag spécifique, idéal pour créer une `pre-prod` depuis une version stable.
   - **Exemple** :
     ```bash
     git checkout -b pre-prod v1.0.0  # Crée pre-prod depuis le tag v1.0.0
     git checkout -b staging HEAD~2   # Crée staging depuis 2 commits en arrière
     ```
   - **Explication DevOps** : Permet de "forker" une version stable pour des tests isolés sans affecter `main`. Utile pour rollback en prod.
   - **Pièges** : Vérifiez l'historique avec `git log --oneline` avant pour éviter de partir d'un état instable.
   - **Intégration CI/CD** : Déclenchez un workflow sur création de `pre-prod` pour des audits de sécurité automatisés.

### 3. **git merge --no-ff <branche>** (Merge sans Fast-Forward)
   - **Description** : Force un commit de merge même si un fast-forward est possible, préservant l'historique des branches pour une traçabilité DevOps.
   - **Exemple** :
     ```bash
     git checkout staging
     git merge --no-ff feature/add-hello-route  # Merge feature dans staging avec un commit dédié
     ```
   - **Explication DevOps** : Crée un historique clair pour audits (ex. : voir quand une feature a été intégrée à staging). Essentiel pour les releases réglementées (ex. : compliance ISO).
   - **Pièges** : Augmente le nombre de commits ; utilisez `--ff-only` pour l'inverse si vous voulez un historique linéaire.
   - **Intégration CI/CD** : Configurez des protections pour exiger `--no-ff` dans les PR vers `staging`.

### 4. **git rebase -i <branche>** (Rebase Interactif)
   - **Description** : Réécrit l'historique interactivement (squash, edit, drop commits). Parfait pour nettoyer une branche `post-merge` avant push.
   - **Exemple** :
     ```bash
     git checkout post-merge
     git rebase -i main  # Ouvre un éditeur pour squash/edit commits
     ```
   - **Explication DevOps** : Rend l'historique propre pour les changelogs automatisés. Utilisez pour combiner des commits triviaux post-fusion.
   - **Pièges** : Ne rebasez jamais des branches publiques (risque de conflits pour l'équipe). Toujours push avec `--force-with-lease` après.
   - **Intégration CI/CD** : Intégrez dans un hook `pre-push` pour valider l'historique.

### 5. **git cherry-pick <commit>** (Sélection de Commits)
   - **Description** : Applique un commit spécifique d'une branche à une autre, idéal pour hotfixes de `pre-prod` vers `staging`.
   - **Exemple** :
     ```bash
     git checkout staging
     git cherry-pick abc1234  # Applique le commit abc1234 de pre-prod à staging
     ```
   - **Explication DevOps** : Permet de propager des correctifs urgents sans merger toute la branche, minimisant les risques en prod.
   - **Pièges** : Peut causer des doublons si le commit est mergé plus tard ; trackez avec des messages clairs.
   - **Intégration CI/CD** : Automatisez via workflow pour cherry-pick sur tags hotfix.

---

## 🏷️ Commandes Avancées pour les Tags

### 1. **git tag -a <tag> -m <message>** (Création de Tag Annoté)
   - **Description** : Crée un tag avec métadonnées, essentiel pour marquer des versions stables en DevOps.
   - **Exemple** :
     ```bash
     git tag -a v2.0.0 -m "Release staging-ready avec audits"  # Tag annoté
     git push origin v2.0.0  # Push le tag
     ```
   - **Explication DevOps** : Tags déclenchent des déploiements (ex. : build Docker sur tag). Utilisez pour versionnement sémantique.
   - **Pièges** : Tags sont immuables ; supprimez et recréez si erreur (`git tag -d <tag>` puis push `--delete`).

### 2. **git describe --tags** (Description de l'État Actuel)
   - **Description** : Fournit une description humaine de la position actuelle par rapport au tag le plus proche.
   - **Exemple** :
     ```bash
     git describe --tags  # Output : v1.0.0-5-gabc123 (5 commits après v1.0.0)
     ```
   - **Explication DevOps** : Utile pour générer des numéros de build automatisés dans CI/CD (ex. : artifact naming).

### 3. **git tag --verify <tag>** (Vérification de Tags Signés)
   - **Description** : Vérifie la signature GPG d'un tag, pour la sécurité en DevOps.
   - **Exemple** :
     ```bash
     git tag -s v2.0.0 -m "Signed release"  # Créer un tag signé
     git tag --verify v2.0.0  # Vérifier
     ```
   - **Explication DevOps** : Assure l'intégrité des releases en environnements sensibles (ex. : fintech).

---

## 🔒 Commandes Avancées pour les Hooks (Pre- et Post-)

### 1. **git hooks** (Gestion des Hooks Locaux)
   - **Description** : Scripts exécutés avant/après des actions Git. Ex. : `pre-commit` pour linting, `post-merge` pour notifications.
   - **Exemple** :
     - Créez `.git/hooks/pre-commit` (fichier exécutable) :
       ```bash
       #!/bin/sh
       pytest tests/  # Exécute tests avant commit
       ```
     - Activez : `chmod +x .git/hooks/pre-commit`
   - **Explication DevOps** : Automatise les validations locales avant push, réduisant les échecs CI.
   - **Pièges** : Hooks sont locaux ; utilisez Husky ou pre-commit framework pour les partager.

### 2. **git config --local core.hooksPath <dossier>** (Hooks Partagés)
   - **Description** : Définit un dossier partagé pour hooks, pour standardiser en équipe.
   - **Exemple** :
     ```bash
     git config --local core.hooksPath .githooks/  # Utilise hooks dans .githooks/
     ```
   - **Explication DevOps** : Permet de versionner les hooks (ex. : post-merge pour update submodules).

---

## 🛑 Pièges Avancés et Bonnes Pratiques DevOps
1. **Force Push Sécurisé** : Utilisez `git push --force-with-lease` pour éviter d'écraser des changements distants.
2. **Submodules pour Dépendances** : `git submodule add <repo> <path>` pour gérer des repos imbriqués en microservices.
3. **Bisect pour Debugging** : `git bisect start <bad> <good>` pour trouver un commit fautif rapidement.
4. **Reflog pour Récupération** : `git reflog` pour voir et restaurer des états perdus (ex. : après rebase raté).
5. **Intégration CI/CD** : Utilisez des webhooks GitHub pour déclencher sur branches spécifiques ; protégez `main` et `staging` avec des règles (require approvals).
6. **Sécurité** : Signez commits/tags avec GPG (`git commit -S`).
7. **Outils Complémentaires** : Git LFS pour fichiers lourds, Git Worktree pour branches parallèles sans switch.

