# Utiliser une image Python légère
FROM python:3.12-slim

# Répertoire de travail
WORKDIR /app

# Copier les dépendances
COPY requirements.txt .

# Installer les dépendances (ex: FastAPI ou Django)
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code source
COPY . .

# Exposer le port
EXPOSE 8000

# Commande par défaut (modifiée en prod via Compose)
CMD ["python", "-m", "http.server", "8000"]
