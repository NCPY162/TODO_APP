# Utiliser une image python comme base
FROM python:3.10-slim

# Définir un répertoire de travail (comme mkdir /app)
WORKDIR /app

# Copier le fichier de configuration pour postgresql et installer les dépendances systèmes
RUN apt-get update && apt-get install -y libpq-dev gcc

# Copier le fichier requirements.txt pour installer les dépendances
COPY requirements.txt .

# Installer les dépendances python nécecessaires au projet
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code du projet dans le conteneur
COPY . .

# Exposer le port 8000
EXPOSE 8000

# Lancer le serveur Django
CMD ["python", "./src/manage.py", "0.0.0.0:8000"]



