#!/bin/bash

# Vérification des arguments
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <nom_de_l_organisation> <nom_du_repertoire>"
    exit 1
fi

# Récupération des arguments
ORG_NAME="$1"
REPO_NAME="$2"

# Vérification des variables d'environnement
if [ -z "$GITHUB_USERNAME" ] || [ -z "$GITHUB_TOKEN" ]; then
    echo "❌ Erreur : Les variables GITHUB_USERNAME et GITHUB_TOKEN doivent être définies."
    exit 1
fi

# URL de base de l'API GitHub
BASE_URL="https://api.github.com/repos/$ORG_NAME/$REPO_NAME"

# Fonction pour gérer les erreurs de requête API
handle_api_error() {
    local http_code="$1"
    local response="$2"
    local message="$3"

    if [ "$http_code" -ne 200 ]; then
        echo "❌ Erreur : Impossible de récupérer $message."
        echo "Code HTTP : $http_code"
        echo "Réponse : $response"
        exit 1
    fi
}

# Récupération des administrateurs
echo "🔍 Récupération des administrateurs du dépôt..."
admins_response=$(curl -s -u "$GITHUB_USERNAME:$GITHUB_TOKEN" -w "%{http_code}" "$BASE_URL/collaborators?affiliation=direct")
admins_http_code="${admins_response: -3}"
admins_json="${admins_response::-3}"

handle_api_error "$admins_http_code" "$admins_json" "la liste des administrateurs"

# Vérification JSON valide
if ! echo "$admins_json" | jq empty 2>/dev/null; then
    echo "❌ Erreur : Réponse JSON invalide pour les administrateurs."
    exit 1
fi

# Création du fichier CSV pour les administrateurs
ADMIN_FILE="admins.csv"
echo "👑 Enregistrement des administrateurs dans $ADMIN_FILE..."
echo "Username" > "$ADMIN_FILE"
echo "$admins_json" | jq -r '.[] | select(.permissions.admin == true) | .login' >> "$ADMIN_FILE"

# Récupération des collaborateurs et permissions
echo "🔍 Récupération des collaborateurs et leurs permissions..."
collaborators_response=$(curl -s -u "$GITHUB_USERNAME:$GITHUB_TOKEN" -w "%{http_code}" "$BASE_URL/collaborators")
collaborators_http_code="${collaborators_response: -3}"
collaborators_json="${collaborators_response::-3}"

handle_api_error "$collaborators_http_code" "$collaborators_json" "la liste des collaborateurs"

# Vérification JSON valide
if ! echo "$collaborators_json" | jq empty 2>/dev/null; then
    echo "❌ Erreur : Réponse JSON invalide pour les collaborateurs."
    exit 1
fi

# Création du fichier CSV pour les collaborateurs
COLLAB_FILE="collaborators.csv"
echo "👥 Enregistrement des collaborateurs dans $COLLAB_FILE..."
echo "Username,Admin,Push,Pull" > "$COLLAB_FILE"
echo "$collaborators_json" | jq -r '.[] | "\(.login),\(.permissions.admin),\(.permissions.push),\(.permissions.pull)"' >> "$COLLAB_FILE"

echo "✅ Données enregistrées avec succès dans $ADMIN_FILE et $COLLAB_FILE"
