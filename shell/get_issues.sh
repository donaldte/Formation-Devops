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

# URL de l'API GitHub pour les issues
API_URL="https://api.github.com/repos/$ORG_NAME/$REPO_NAME/issues"

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

# Récupération des issues
echo "🔍 Récupération des issues du dépôt..."
issues_response=$(curl -s -u "$GITHUB_USERNAME:$GITHUB_TOKEN" -w "%{http_code}" "$API_URL")
issues_http_code="${issues_response: -3}"
issues_json="${issues_response::-3}"

handle_api_error "$issues_http_code" "$issues_json" "la liste des issues"

# Vérification JSON valide
if ! echo "$issues_json" | jq empty 2>/dev/null; then
    echo "❌ Erreur : Réponse JSON invalide pour les issues."
    exit 1
fi

# Création du fichier CSV
ISSUES_FILE="issues.csv"
echo "📄 Enregistrement des issues dans $ISSUES_FILE..."
echo "Issue Number,Auteur,Titre,Date de création,Statut,Tags" > "$ISSUES_FILE"

echo "$issues_json" | jq -r '
    .[] | "\(.number),\(.user.login),\"\(.title)\",\(.created_at),\(.state),\"\(.labels | map(.name) | join(", "))\""
' >> "$ISSUES_FILE"

echo "✅ Données enregistrées avec succès dans $ISSUES_FILE"
