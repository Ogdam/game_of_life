FROM node:20-slim

WORKDIR /frontend

# Copie des fichiers de configuration du package
COPY ./gol-fe/package*.json ./

RUN npm install

# Copie de tout le reste du projet Vite
COPY ./gol-fe/ .

# Vite tourne par défaut sur le port 5173
EXPOSE 5173

# Le --host est indispensable pour que Docker puisse rediriger le port
CMD ["npm", "run", "dev", "--", "--host"]