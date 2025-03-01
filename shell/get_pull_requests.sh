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

# URL de l'API GitHub pour les pull requests
API_URL="https://api.github.com/repos/$ORG_NAME/$REPO_NAME/pulls"

# Fonction pour gérer les erreurs API
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

# Récupération des pull requests
echo "🔍 Récupération des pull requests du dépôt..."
pulls_response=$(curl -s -u "$GITHUB_USERNAME:$GITHUB_TOKEN" -w "%{http_code}" "$API_URL")
pulls_http_code="${pulls_response: -3}"
pulls_json="${pulls_response::-3}"

handle_api_error "$pulls_http_code" "$pulls_json" "la liste des pull requests"

# Vérification JSON valide
if ! echo "$pulls_json" | jq empty 2>/dev/null; then
    echo "❌ Erreur : Réponse JSON invalide pour les pull requests."
    exit 1
fi

# Création du fichier CSV
PULLS_FILE="pull_requests.csv"
echo "👥 Enregistrement des pull requests dans $PULLS_FILE..."
echo "PR Number,Auteur,Titre,Message,Date de création" > "$PULLS_FILE"
echo "$pulls_json" | jq -r '.[] | "\(.number),\(.user.login),\"\(.title)\",\"\(.body)\",\(.created_at)" ' >> "$PULLS_FILE"

echo "✅ Données enregistrées avec succès dans $PULLS_FILE"
