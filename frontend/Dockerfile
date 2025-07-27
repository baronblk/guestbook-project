# Multi-stage build für optimierte Production-Builds
FROM node:18-alpine AS builder

WORKDIR /app

# Package files kopieren und installieren
COPY package*.json ./
RUN npm ci --only=production

# Source Code kopieren
COPY . .

# Production Build erstellen
RUN npm run build

# Production Stage mit Nginx
FROM nginx:alpine

# Custom nginx config kopieren
COPY --from=builder /app/build /usr/share/nginx/html

# Nginx-Konfiguration für React SPA
RUN echo 'server { \
    listen 80; \
    server_name localhost; \
    location / { \
        root /usr/share/nginx/html; \
        index index.html index.htm; \
        try_files $uri $uri/ /index.html; \
    } \
    location /api/ { \
        proxy_pass http://backend:8000/api/; \
        proxy_set_header Host $host; \
        proxy_set_header X-Real-IP $remote_addr; \
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for; \
        proxy_set_header X-Forwarded-Proto $scheme; \
    } \
}' > /etc/nginx/conf.d/default.conf

# Port freigeben
EXPOSE 80

# Nginx starten
CMD ["nginx", "-g", "daemon off;"]
