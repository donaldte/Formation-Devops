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

# URL de l'API GitHub
API_URL="https://api.github.com/repos/$ORG_NAME/$REPO_NAME"

# Fonction pour gérer les erreurs API 
handle_api_error() {
    local http_code="$1"
    local response="$2"
    local message="$3"

    if [ "$http_code" -ne 200 ] && [ "$http_code" -ne 201 ]; then 
        echo "❌ Erreur : Impossible de $message."
        echo "Code HTTP : $http_code"
        echo "Réponse : $response"
        exit 1
    fi
}

# 1️⃣ Récupération des labels disponibles
echo "🔍 Récupération des labels disponibles..."
labels_response=$(curl -s -u "$GITHUB_USERNAME:$GITHUB_TOKEN" -w "%{http_code}" "$API_URL/labels")
labels_http_code="${labels_response: -3}"
labels_json="${labels_response::-3}"

handle_api_error "$labels_http_code" "$labels_json" "récupérer les labels"

# Affichage des labels disponibles
labels_list=$(echo "$labels_json" | jq -r '.[].name')
if [ -z "$labels_list" ]; then
    echo "⚠️ Aucun label trouvé dans ce dépôt."
else
    echo "📌 Labels disponibles :"
    echo "$labels_list"
fi

# 2️⃣ Demande d'informations à l'utilisateur
echo "📝 Création d'une nouvelle issue..."

read -p "📌 Entrez le titre de l'issue : " ISSUE_TITLE
read -p "📖 Entrez la description de l'issue : " ISSUE_BODY
read -p "🏷️ Sélectionnez un label (optionnel, laissez vide si aucun) : " SELECTED_LABEL

# Vérification si l'utilisateur a sélectionné un label valide
# -n vérifie si la chaîne n'est pas vide
if [[ -n "$SELECTED_LABEL" ]] && ! echo "$labels_list" | grep -Fxq "$SELECTED_LABEL"; then
    echo "⚠️ Le label sélectionné n'existe pas. Il sera ignoré."
    SELECTED_LABEL=""
fi

# 3️⃣ Création de l'issue via l'API GitHub
echo "🚀 Envoi de l'issue à GitHub..."
if [[ -z "$SELECTED_LABEL" ]]; then
    issue_data=$(jq -n --arg title "$ISSUE_TITLE" --arg body "$ISSUE_BODY" \
        '{title: $title, body: $body}')
else
    issue_data=$(jq -n --arg title "$ISSUE_TITLE" --arg body "$ISSUE_BODY" --arg label "$SELECTED_LABEL" \
        '{title: $title, body: $body, labels: [$label]}')
fi

create_issue_response=$(curl -s -u "$GITHUB_USERNAME:$GITHUB_TOKEN" -X POST -w "%{http_code}" \
    -H "Accept: application/vnd.github.v3+json" \
    -d "$issue_data" "$API_URL/issues")

create_issue_http_code="${create_issue_response: -3}"
create_issue_json="${create_issue_response::-3}"

handle_api_error "$create_issue_http_code" "$create_issue_json" "créer l'issue"

# 4️⃣ Affichage du lien de l'issue créée
issue_url=$(echo "$create_issue_json" | jq -r '.html_url')
echo "✅ Issue créée avec succès : $issue_url"
