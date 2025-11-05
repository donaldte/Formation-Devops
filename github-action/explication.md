CI/CD avec Github Actions
ci: 
    - build (image docker)
    - test(unittest, integrationtest, lint)

cd: 
    - deploy

# Github Actions 
  - definition de github actions : 
    - c'est une plateforme de ci/cd vous permettant d'automatiser le build, le test et le déploiement de vos applications

1 ton projet doit avoir un repository github: 
  - créer un repository github
  - ajouter un dossier .github/workflows
  - creer les fichier YAML 
  - ajouter des declancher(schedule, event, manuel) au actions

2 workflow: 
  - ci workflow 
  - deployment workflow 
  - automate workflow 
  - code scanning workflow
  - pages workflow

3 les jobs (build, test, deploy, etc..)
  - un workflow est composé de jobs
    - un job est composé de steps
      - un step est composé de runs
        - un run est composé de commands
          - un command est composé de args


4- les Event:
  - push(su quelle branche)
    - push sur le master
      - declancher un workflow 
  - pull_request (sur quelle branche)
    - declancher un workflow


5- runners (machine virtuelle):
   - github runners
   - docker runners
   - self hosted runners

6 - actions: 
   - actions are reusable
     - actions are composable
     - actions are extensible


# CONCEPTS GITHUB ACTIONS
 
 1- workflow: 
     - c'est un processus d'automatisation de tâche
     - c'est un fichier YAML (.yml, yaml)
     - c'est composé de jobs
  - trigger: 
    - push, pull_request, schedule, workflow_dispatch, manuel etc..

2- les variables 
   - variable workflow : env 
   - variable d'environnement (dev, staging, prod)
   - variable d'organistation
   - variable du repetoire

# CONCEPTS GITHUB ACTIONS 
   1- workflow: 
       - c'est un processus d'automatisation de tâche (job) fichier YAML (.yml, yaml)
       - c'est composé de jobs(build, test, deploy, etc..)
       -les jobs sont composé de steps
         - les steps sont composé de runs
           - les runs sont composé de commands
             - les commands sont composé de args

    2- variable
        -variable du workflow: 
            - env
        -variable d'environnement: 
            - dev, staging, prod (ici tu crees d'abord les environnements)
        -variable d'organistation: 
            - github
        -variable du repetoire: 
            - owner, repo
        - variable par defaut 
            - github.actor
            - github.repository
            - github.sha
            - github.event_name
            - github.ref
            - github.head_ref
            - github.base_ref
            - github.server_url
            - github.api_url
            - github.graphql_url
        - creer une variable d'environement dans le workflow 
        echo "MY_VAR=my_value" >> $GITHUB_ENV
         pour acceder ${{ github.MY_VAR }}
    3- Expression: 
        - ${{ github.actor }}
        - ${{ github.repository }}
        - ${{ if github.ref == 'refs/heads/main' }}
        - ${{ env.MY_VAR }}
        - ${{ secrets.MY_SECRET }}
        - ${{ vars.MY_VAR }}

    4- les workflow reutilisable     
       - eviter de repeter les actions
       - permet de faire des actions communes
       - facilite la maintenance

    5- enviroment de deploiement
      - dev, staging, prod

    6- artefact 
      - c'est le output de des jobs(zip, tar, logs, etc..)

    7- cache de dependances 
      - maven , npm, pip, gradle, etc..

# SYSNTAXE DU WORKFLOW 

 on:
    label: 
      - action 


* 1 * * 1,2      
le premier c'est les minute (0 - 59)
le second c'est les heures (0 - 23)
le troisieme c'est les jours du mois (0 - 31)
le quatrieme c'est les mois (1- 12)
le cinquieme c'est les jours de la semaine (0 - 6 or SUN-SAT)

* * * * * 
on:
  schedule:
    - cron: '0 0 * * *'

            