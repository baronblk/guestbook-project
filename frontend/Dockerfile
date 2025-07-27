FROM node:18-alpine

WORKDIR /app

# Package files kopieren und installieren
COPY package*.json ./
RUN npm install

# Source Code kopieren
COPY . .

# Port freigeben
EXPOSE 3000

# Development Server starten
CMD ["npm", "start"]
