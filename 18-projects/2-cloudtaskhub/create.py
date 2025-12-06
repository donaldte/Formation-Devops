# create_helm_structure.py

import os

# Dossier racine
root = "helm"

# Liste des microservices / composants
folders = [
    "gateway",
    "auth",
    "project",
    "billing",
    "notification",
    "analytics",
    "kafka",
    "jaeger",
    "prometheus",
    "grafana"
]

# Création du dossier racine s’il n’existe pas
os.makedirs(root, exist_ok=True)

# Création de chaque dossier avec une structure Helm de base
for folder in folders:
    path = os.path.join(root, folder)
    
    # Dossiers principaux du chart
    os.makedirs(path, exist_ok=True)
    os.makedirs(os.path.join(path, "templates"), exist_ok=True)
    os.makedirs(os.path.join(path, "charts"), exist_ok=True)  # pour les sous-charts si besoin
    
    # Fichiers de base Helm
    chart_yaml = os.path.join(path, "Chart.yaml")
    values_yaml = os.path.join(path, "values.yaml")
    
    helpers_tpl = os.path.join(path, "templates", "_helpers.tpl")
    notes_txt = os.path.join(path, "templates", "NOTES.txt")
    
    # Création du Chart.yaml minimal si pas déjà présent
    if not os.path.exists(chart_yaml):
        with open(chart_yaml, "w") as f:
            f.write(f"""apiVersion: v2
name: {folder}
description: Helm chart pour le microservice {folder}
type: application
version: 0.1.0
appVersion: "1.0.0"
""")
    
    # values.yaml vide ou avec commentaire
    if not os.path.exists(values_yaml):
        with open(values_yaml, "w") as f:
            f.write(f"# Valeurs par défaut pour {folder}\nreplicaCount: 1\n")
    
    # _helpers.tpl vide
    if not os.path.exists(helpers_tpl):
        open(helpers_tpl, "w").close()
    
    # NOTES.txt
    if not os.path.exists(notes_txt):
        with open(notes_txt, "w") as f:
            f.write(f"Chart {folder} installé avec succès !\n")

    print(f"Chart créé → {path}")

print("\nArborescence Helm prête !")
print("Tu peux maintenant faire tes premiers :")
print("  cd helm/auth && helm install auth . --dry-run")