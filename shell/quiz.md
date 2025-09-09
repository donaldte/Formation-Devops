
### Quiz d'Évaluation : Concepts de Base en DevOps (60 Questions)

1. Dans le contexte d'une pratique DevOps CI/CD, quel est le rôle principal d'un workflow GitHub Actions pour une application Django ?  
   A) Exécuter uniquement des tests unitaires sur le serveur local.  
   B) Automatiser les tests, le build et le déploiement sur un VPS distant.  
   C) Gérer les backups de la base de données PostgreSQL.  
   D) Installer manuellement les dépendances Python sur le serveur.

2. En DevOps, quelle est la différence clé entre CI (Continuous Integration) et CD (Continuous Deployment) dans un pipeline comme celui pour Django ?  
   A) CI se concentre sur l'intégration et les tests automatisés ; CD sur le déploiement automatisé en production.  
   B) CI gère les connexions SSH ; CD installe les environnements virtuels.  
   C) CI utilise Docker pour les bases de données ; CD pour les serveurs web.  
   D) CI est pour les débutants ; CD pour les experts.

3. Sur un serveur Linux comme AWS EC2 (Ubuntu), quelle commande met à jour la liste des paquets disponibles avant d'installer des logiciels ?  
   A) `sudo yum update`  
   B) `sudo apt update`  
   C) `sudo pip install --upgrade`  
   D) `sudo git pull`

4. Dans le shell Bash sur Linux, quelle commande crée un répertoire `/var/www/mon-app-django` et change son propriétaire pour l'utilisateur courant (sans sudo pour les sous-dossiers) ?  
   A) `mkdir /var/www/mon-app-django && chown $USER:$USER /var/www/mon-app-django`  
   B) `touch /var/www/mon-app-django && chmod 777 /var/www/`  
   C) `ls -la /var/www/ && sudo rm -rf mon-app-django`  
   D) `cd /var/www/ && git init mon-app-django`

5. Pour une pratique DevOps sécurisée sur Linux, quelles permissions doit-on appliquer à un fichier de clé SSH privée (`~/.ssh/id_ed25519`) pour éviter les erreurs de connexion ?  
   A) `chmod 777 ~/.ssh/id_ed25519`  
   B) `chmod 600 ~/.ssh/id_ed25519`  
   C) `chmod 644 ~/.ssh/id_ed25519`  
   D) `chmod 000 ~/.ssh/id_ed25519`

6. En GitHub Actions, quelle section du fichier YAML définit quand le workflow s'exécute, par exemple sur un push vers la branche `master` ?  
   A) `jobs:`  
   B) `on:`  
   C) `steps:`  
   D) `secrets:`

7. Dans un workflow GitHub Actions pour Django, quelle action utilise-t-on pour cloner le dépôt dans le runner (VM) ?  
   A) `uses: actions/setup-python@v4`  
   B) `uses: actions/checkout@v4`  
   C) `uses: dawidd6/action-send-mail@v4`  
   D) `uses: actions/upload-artifact@v4`

8. Pour configurer un service PostgreSQL dans un job de test GitHub Actions, quel bloc YAML définit un conteneur Docker avec des variables d'environnement comme `POSTGRES_USER` ?  
   A) `env:`  
   B) `services:`  
   C) `with:`  
   D) `run:`

9. En shell scripting dans GitHub Actions, quelle commande active un environnement virtuel Python (`venv`) dans une étape de test ou de déploiement ?  
   A) `pip install -r requirements.txt`  
   B) `source venv/bin/activate`  
   C) `python -m venv venv`  
   D) `deactivate`

10. Quelle est la commande shell pour générer une paire de clés SSH Ed25519, comme recommandé pour les connexions sécurisées à un VPS EC2 ?  
    A) `ssh-keygen -t rsa -b 2048`  
    B) `ssh-keygen -t ed25519 -C "email@example.com"`  
    C) `openssl genrsa -out private.key 2048`  
    D) `ssh-add -l`

11. Sur un serveur Linux, où stocke-t-on la clé publique SSH pour autoriser les connexions sans mot de passe depuis GitHub Actions ?  
    A) Dans GitHub Secrets comme `VPS_SSH_KEY`.  
    B) Dans `~/.ssh/id_ed25519.pub` localement.  
    C) In `~/.ssh/authorized_keys` sur le serveur.  
    D) Dans `/var/www/.env`.

12. Dans GitHub Actions, quel secret stocke-t-on pour permettre la connexion SSH au VPS (contenant la clé privée entière en PEM) ?  
    A) `VPS_PUBLIC_KEY`  
    B) `VPS_SSH_KEY`  
    C) `DATABASE_URL`  
    D) `EMAIL_PASSWORD`

13. En pratique DevOps avec Linux, quelle commande installe Docker sur Ubuntu (EC2) pour héberger PostgreSQL en conteneur ?  
    A) `sudo apt install docker.io`  
    B) `curl -fsSL https://get.docker.com | sudo sh`  
    C) `pip install docker`  
    D) `sudo yum install docker-ce`

14. Dans le shell, quelle commande ajoute l'utilisateur courant au groupe Docker pour exécuter des conteneurs sans sudo ?  
    A) `sudo usermod -aG docker $USER && newgrp docker`  
    B) `sudo chmod +x /usr/bin/docker`  
    C) `docker groupadd docker`  
    D) `sudo docker login`

15. Pour un fichier `.env` en DevOps Django sur serveur Linux, quelle pratique évite de commiter des secrets comme `SECRET_KEY` ?  
    A) Ajoutez `.env` à `.gitignore` et chargez-le via `environ.Env.read_env()` dans `settings.py`.  
    B) Commettez `.env` mais chiffrez-le avec Git Crypt.  
    C) Utilisez `requirements.txt` pour les secrets.  
    D) Stockez en dur dans `settings.py`.

16. En GitHub Actions, quelle expression conditionnelle exécute une étape d'envoi d'email seulement si le job échoue ?  
    A) `if: always()`  
    B) `if: success()`  
    C) `if: failure()`  
    D) `if: github.ref == 'master'`

17. Dans une étape de déploiement SSH GitHub Actions, quel flag bash (`set -e`) arrête le script en cas d'erreur lors d'un `git pull` ou `migrate` ?  
    A) `set -x`  
    B) `set -e`  
    C) `set -u`  
    D) `set +e`

18. Sur Linux, quelle commande lance un conteneur PostgreSQL Docker en arrière-plan avec persistance de données via volume ?  
    A) `docker run -d postgres:16`  
    B) `sudo docker run --name postgres16 -e POSTGRES_DB=mydb -p 5432:5432 -v /data:/var/lib/postgresql/data postgres:16`  
    C) `docker pull postgres:16 && docker exec -it postgres16`  
    D) `docker-compose up postgres`

19. En DevOps, pour vérifier les permissions sur `/var/www/` après clonage d'un repo Django, quelle commande shell liste les propriétaires et droits ?  
    A) `ls -la /var/www/`  
    B) `sudo find /var/www/ -type d`  
    C) `git status /var/www/`  
    D) `chown -R www-data /var/www/`

20. Dans GitHub Actions pour notifier un échec de déploiement Django, quel input de l'action `dawidd6/action-send-mail` attache un fichier de rapport de tests ?  
    A) `body:`  
    B) `subject:`  
    C) `attachments: test_report.txt`  
    D) `to: team@example.com`


21. Dans un script Bash pour le déploiement Django (`deploy.sh`), quelle commande vérifie si un environnement virtuel existe avant de l'activer ?  
    A) `if [ -d venv ]; then source venv/bin/activate; fi`  
    B) `source venv/bin/activate`  
    C) `python -m venv venv`  
    D) `ls venv && activate venv`

22. En Linux, quelle commande shell affiche la variable d'environnement `PATH` pour vérifier si Python est accessible après activation d'un venv ?  
    A) `echo $PATH`  
    B) `printenv PYTHONPATH`  
    C) `which python`  
    D) `export PATH`

23. Dans GitHub Actions, quelle variable de contexte contient le nom de la branche en cours (e.g., `master`) pour personnaliser un déploiement ?  
    A) `${{ github.sha }}`  
    B) `${{ github.ref_name }}`  
    C) `${{ github.actor }}`  
    D) `${{ github.run_id }}`

24. Pour sécuriser un serveur EC2 Linux, quelle modification dans `/etc/ssh/sshd_config` désactive les connexions SSH root ?  
    A) `PermitRootLogin no`  
    B) `PasswordAuthentication yes`  
    C) `AllowUsers root`  
    D) `Port 2222`

25. Dans un script Bash de déploiement, quelle commande vérifie si `git pull` a réussi avant de continuer avec `python manage.py migrate` ?  
    A) `git pull && echo "Success"`  
    B) `if git pull; then python manage.py migrate; fi`  
    C) `git status | grep origin`  
    D) `git pull --force`

26. En DevOps, pourquoi est-il recommandé d'utiliser `pip install -r requirements.txt` dans un environnement virtuel sur le serveur ?  
    A) Pour installer globalement les paquets Python.  
    B) Pour isoler les dépendances du projet et éviter les conflits.  
    C) Pour compiler Django en bytecode.  
    D) Pour créer un backup des dépendances.

27. Dans GitHub Actions, quelle option dans `actions/setup-python@v4` active le cache des dépendances pip pour accélérer les installations ?  
    A) `cache: 'pip'`  
    B) `cache: 'venv'`  
    C) `cache: 'requirements.txt'`  
    D) `cache: 'python'`

28. En shell Bash, quelle commande redirige à la fois stdout et stderr vers un fichier `deploy.log` dans un script de déploiement ?  
    A) `./deploy.sh > deploy.log`  
    B) `./deploy.sh 2>&1 > deploy.log`  
    C) `./deploy.sh >> deploy.log 2>&1`  
    D) `./deploy.sh | tee deploy.log`

29. Sur un serveur Linux, quelle commande vérifie si le service Gunicorn (utilisé pour Django) est en cours d'exécution ?  
    A) `sudo systemctl status gunicorn`  
    B) `ps aux | grep python`  
    C) `sudo service gunicorn restart`  
    D) `docker ps -f name=gunicorn`

30. Dans un fichier `.env` pour Django, quelle variable configure les hôtes autorisés pour éviter l'erreur `Invalid HTTP_HOST header` ?  
    A) `SECRET_KEY`  
    B) `ALLOWED_HOSTS`  
    C) `DATABASE_URL`  
    D) `DEBUG`

31. En GitHub Actions, quel paramètre dans `actions/checkout@v4` récupère l'historique Git complet pour permettre `git log` dans une étape ?  
    A) `fetch-depth: 0`  
    B) `history: full`  
    C) `depth: unlimited`  
    D) `clone: true`

32. Dans un script Bash, quelle commande teste si un fichier `requirements.txt` existe avant d'exécuter `pip install` ?  
    A) `if [ -f requirements.txt ]; then pip install -r requirements.txt; fi`  
    B) `test requirements.txt && pip install`  
    C) `ls requirements.txt || exit 1`  
    D) `find requirements.txt -exec pip install {}`

33. Sur Linux, quelle commande shell vérifie si le port 5432 (Postgres) est ouvert avant de lancer des migrations Django ?  
    A) `netstat -tuln | grep 5432`  
    B) `ping localhost:5432`  
    C) `telnet 5432`  
    D) `curl localhost:5432`

34. En DevOps, quelle pratique améliore la sécurité des secrets GitHub Actions comme `VPS_SSH_KEY` ?  
    A) Stocker les secrets en clair dans le YAML.  
    B) Utiliser des secrets de dépôt dans Settings > Secrets and variables > Actions.  
    C) Ajouter les secrets dans `.gitignore`.  
    D) Partager les secrets via email.

35. Dans un script Bash pour `deploy.sh`, quelle commande rend un script exécutable avant de l'appeler ?  
    A) `chmod +x deploy.sh`  
    B) `chown deploy.sh`  
    C) `touch deploy.sh`  
    D) `bash deploy.sh`

36. En GitHub Actions, quelle variable d'environnement spéciale permet de définir des variables pour toutes les étapes d'un job ?  
    A) `$GITHUB_ENV`  
    B) `$PATH`  
    C) `$GITHUB_OUTPUT`  
    D) `$ENV`

37. Sur un serveur Linux, quelle commande shell sauvegarde la base de données PostgreSQL dans un fichier `backup.sql` ?  
    A) `docker exec postgres16 pg_dump -U myuser mydatabase > backup.sql`  
    B) `psql -U myuser -d mydatabase > backup.sql`  
    C) `docker cp postgres16:/backup.sql .`  
    D) `pg_restore mydatabase > backup.sql`

38. Dans un workflow GitHub Actions, quelle option dans une étape SSH empêche l'interruption si la connexion est lente ?  
    A) `ServerAliveInterval=60`  
    B) `StrictHostKeyChecking=yes`  
    C) `ConnectTimeout=10`  
    D) `BatchMode=no`

39. En shell scripting, quelle commande vérifie si une variable d'environnement `DATABASE_URL` est définie avant de lancer `manage.py migrate` ?  
    A) `if [ -z "$DATABASE_URL" ]; then echo "Error"; exit 1; fi`  
    B) `echo $DATABASE_URL | grep url`  
    C) `export DATABASE_URL && migrate`  
    D) `test $DATABASE_URL || migrate`

40. Dans GitHub Actions, pourquoi utilise-t-on `continue-on-error: true` pour une étape d'envoi d'email ?  
    A) Pour ignorer les erreurs de connexion SMTP sans arrêter le job.  
    B) Pour relancer l'email en boucle jusqu'à succès.  
    C) Pour forcer l'envoi même si les tests réussissent.  
    D) Pour stocker l'email dans un artifact.

41. Sur Linux, quelle commande shell affiche les 10 dernières lignes du fichier `deploy.log` pour déboguer un déploiement Django ?  
    A) `tail -n 10 deploy.log`  
    B) `cat deploy.log | head -n 10`  
    C) `grep deploy.log -n 10`  
    D) `less deploy.log`

42. En DevOps, quelle commande Docker arrête et supprime un conteneur PostgreSQL nommé `postgres16` ?  
    A) `docker stop postgres16 && docker rm postgres16`  
    B) `docker kill postgres16`  
    C) `docker pause postgres16`  
    D) `docker delete postgres16`

43. Dans un script Bash, quelle syntaxe redirige la sortie d'une commande `git pull` vers `/dev/null` pour la rendre silencieuse ?  
    A) `git pull > /dev/null 2>&1`  
    B) `git pull | silent`  
    C) `git pull --quiet`  
    D) `git pull >> /dev/null`

44. En GitHub Actions, quelle expression récupère l'email de l'auteur du dernier commit pour une notification ?  
    A) `${{ github.actor }}`  
    B) `${{ github.event.head_commit.author.email }}`  
    C) `${{ github.repository }}`  
    D) `${{ github.run_number }}`

45. Sur Linux, quelle commande shell vérifie si un processus `gunicorn` est en cours avant de le redémarrer ?  
    A) `pgrep -f gunicorn`  
    B) `ps aux | grep python`  
    C) `systemctl status gunicorn`  
    D) `killall gunicorn`

46. Dans un fichier `.env` pour Django, quelle valeur de `DEBUG` est recommandée pour un serveur de production ?  
    A) `DEBUG=True`  
    B) `DEBUG=False`  
    C) `DEBUG=1`  
    D) `DEBUG=production`

47. Dans un script Bash de déploiement, quelle commande exécute `deploy.sh` en arrière-plan tout en enregistrant les logs ?  
    A) `nohup ./deploy.sh > deploy.log 2>&1 &`  
    B) `./deploy.sh >> deploy.log`  
    C) `bash deploy.sh &`  
    D) `nohup ./deploy.sh | tee deploy.log`

48. En GitHub Actions, quelle section YAML limite l'exécution d'un job de déploiement uniquement à la branche `master` ?  
    A) `on: push: branches: ['master']`  
    B) `if: github.ref == 'refs/heads/master'`  
    C) `concurrency: master`  
    D) `needs: master`

49. Sur Linux, quelle commande shell change récursivement le propriétaire d'un dossier `/var/www/mon-app-django` à `www-data` pour Nginx ?  
    A) `sudo chown -R www-data:www-data /var/www/mon-app-django`  
    B) `chmod -R 755 /var/www/mon-app-django`  
    C) `chown www-data /var/www/*`  
    D) `sudo mv /var/www/mon-app-django www-data`

50. Dans un workflow GitHub Actions, quelle action télécharge un artifact (e.g., `test_report.txt`) créé dans un job précédent ?  
    A) `actions/upload-artifact@v4`  
    B) `actions/download-artifact@v4`  
    C) `actions/checkout@v4`  
    D) `actions/cache@v4`

51. En shell Bash, quelle commande vérifie si une commande précédente (e.g., `pip install`) a réussi avant de continuer ?  
    A) `if [ $? -eq 0 ]; then echo "Success"; fi`  
    B) `check_status || exit 1`  
    C) `success && echo "OK"`  
    D) `if [ $! == 0 ]; then exit; fi`

52. En DevOps, quelle commande Docker affiche les logs d'un conteneur `postgres16` pour déboguer une erreur de connexion ?  
    A) `docker logs postgres16`  
    B) `docker inspect postgres16`  
    C) `docker ps -a`  
    D) `docker exec -it postgres16 log`

53. Dans un script Bash, quelle commande exporte une variable d'environnement `APP_ENV=production` pour une session ?  
    A) `export APP_ENV=production`  
    B) `set APP_ENV=production`  
    C) `env APP_ENV=production`  
    D) `APP_ENV=production && save`

54. En GitHub Actions, quel bloc YAML définit des variables d'environnement globales pour tout un job ?  
    A) `env:`  
    B) `services:`  
    C) `with:`  
    D) `run:`

55. Sur Linux, quelle commande shell teste la connexion à PostgreSQL (port 5432) sur localhost avant de lancer des migrations ?  
    A) `pg_isready -h localhost -p 5432`  
    B) `curl localhost:5432`  
    C) `netstat -tuln 5432`  
    D) `ping postgres:5432`

56. Dans un script Bash, quelle syntaxe exécute une commande seulement si l'utilisateur courant est `ubuntu` ?  
    A) `if [ "$USER" = "ubuntu" ]; then echo "Ubuntu user"; fi`  
    B) `check_user ubuntu && echo "OK"`  
    C) `whoami == ubuntu && echo "Ubuntu"`  
    D) `if $USER == ubuntu; then echo "User"; fi`

57. En DevOps, pourquoi utilise-t-on `nohup` dans un script de déploiement comme `nohup ./deploy.sh > deploy.log 2>&1` ?  
    A) Pour compresser les logs.  
    B) Pour exécuter la commande même après déconnexion SSH.  
    C) Pour arrêter le script en cas d'erreur.  
    D) Pour limiter l'exécution à 60 secondes.

58. Dans GitHub Actions, quelle variable de contexte contient l'URL du dépôt (e.g., `https://github.com/user/repo`) ?  
    A) `${{ github.repository }}`  
    B) `${{ github.server_url }}/${{ github.repository }}`  
    C) `${{ github.event_name }}`  
    D) `${{ github.workflow }}`

59. Sur Linux, quelle commande shell supprime les fichiers `__pycache__` dans `/var/www/mon-app-django` avant un déploiement ?  
    A) `find /var/www/mon-app-django -name "__pycache__" -type d -exec rm -rf {} +`  
    B) `rm -rf /var/www/mon-app-django/*.pyc`  
    C) `delete __pycache__ /var/www/`  
    D) `find /var/www/ -name "*.py" -delete`

60. En GitHub Actions, quelle option dans `actions/upload-artifact@v4` définit combien de temps un artifact (e.g., `test_report.txt`) est conservé ?  
    A) `retention-days: 7`  
    B) `expire-in: 7d`  
    C) `keep-for: 7`  
    D) `archive: true`

---

### Réponses Expliquées

#### Original 20 Questions
1. **B** : Le workflow automatise tests (CI) et déploiement (CD) sur VPS, comme configuré dans le YAML.
2. **A** : CI intègre/tests code ; CD déploie automatiquement, comme dans le job `deploy`.
3. **B** : `apt update` rafraîchit les paquets sur Ubuntu (EC2), contrairement à `yum` (Amazon Linux).
4. **A** : `mkdir` crée ; `chown $USER:$USER` donne permissions utilisateur courant.
5. **B** : `chmod 600` sécurise la clé SSH privée (lecture/écriture proprio seulement).
6. **B** : `on:` définit les triggers (push, PR, etc.) dans YAML.
7. **B** : `actions/checkout@v4` clone le repo pour CI/CD.
8. **B** : `services:` configure conteneurs Docker comme Postgres pour tests.
9. **B** : `source venv/bin/activate` active le venv dans shell.
10. **B** : `ssh-keygen -t ed25519` génère clé moderne, comme recommandé.
11. **C** : `authorized_keys` sur serveur autorise connexions SSH.
12. **B** : `VPS_SSH_KEY` contient clé privée dans GitHub Secrets.
13. **B** : Script officiel Docker (`get.docker.com`) installe proprement.
14. **A** : `usermod -aG docker` ajoute user ; `newgrp` applique immédiatement.
15. **A** : `.gitignore` protège `.env` ; `django-environ` charge variables.
16. **C** : `if: failure()` exécute étape si job échoue (e.g., email échec).
17. **B** : `set -e` stoppe script sur erreur dans heredoc SSH.
18. **B** : Docker run avec `-v` persiste données Postgres.
19. **A** : `ls -la` montre propriétaires/droits pour `/var/www/`.
20. **C** : `attachments:` joint fichiers dans action email.
21. **A** : `if [ -d venv ]` teste si répertoire venv existe ; `source` active.
22. **A** : `echo $PATH` affiche chemin système, incluant Python après venv.
23. **B** : `${{ github.ref_name }}` donne nom branche (e.g., `master`).
24. **A** : `PermitRootLogin no` désactive login root dans SSH config.
25. **B** : `if git pull; then ...` conditionne migration sur succès pull.
26. **B** : Venv isole dépendances, évite conflits avec système.
27. **A** : `cache: 'pip'` utilise `requirements.txt` pour cache pip.
28. **C** : `>> deploy.log 2>&1` redirige stdout/stderr, append mode.
29. **A** : `systemctl status gunicorn` vérifie état service.
30. **B** : `ALLOWED_HOSTS` configure hôtes valides dans `.env`.
31. **A** : `fetch-depth: 0` récupère tout historique Git.
32. **A** : `if [ -f requirements.txt ]` teste existence fichier.
33. **A** : `netstat -tuln` vérifie ports ouverts (5432 pour Postgres).
34. **B** : Secrets GitHub sécurisent clés SSH/mots de passe.
35. **A** : `chmod +x` rend script exécutable.
36. **A** : `$GITHUB_ENV` définit variables pour job (e.g., `COMMIT_HASH`).
37. **A** : `pg_dump` exporte DB Postgres dans `backup.sql`.
38. **A** : `ServerAliveInterval=60` maintient connexion SSH active.
39. **A** : `if [ -z "$DATABASE_URL" ]` teste si variable vide.
40. **A** : `continue-on-error: true` ignore erreurs email sans arrêter job.
41. **A** : `tail -n 10` montre dernières lignes pour débogage.
42. **A** : `docker stop && rm` arrête/supprime conteneur.
43. **A** : `> /dev/null 2>&1` redirige tout output pour silence.
44. **B** : `${{ github.event.head_commit.author.email }}` donne email auteur.
45. **A** : `pgrep -f gunicorn` trouve processus Gunicorn.
46. **B** : `DEBUG=False` sécurise prod (pas de traces stack).
47. **A** : `nohup ... &` exécute en arrière-plan avec logs.
48. **B** : `if: github.ref` limite job à branche `master`.
49. **A** : `chown -R` change proprio récursivement pour Nginx.
50. **B** : `download-artifact@v4` récupère artifacts (e.g., rapport).
51. **A** : `$?` contient code retour dernière commande.
52. **A** : `docker logs` montre logs conteneur Postgres.
53. **A** : `export` définit variable pour session shell.
54. **A** : `env:` définit variables globales dans job YAML.
55. **A** : `pg_isready` teste connexion Postgres sur port.
56. **A** : `if [ "$USER" = "ubuntu" ]` compare utilisateur courant.
57. **B** : `nohup` persiste commande après déconnexion SSH.
58. **B** : `${{ github.server_url }}/${{ github.repository }}` forme URL dépôt.
59. **A** : `find -exec rm` supprime dossiers `__pycache__` récursivement.
60. **A** : `retention-days` contrôle durée conservation artifact.