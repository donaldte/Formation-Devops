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