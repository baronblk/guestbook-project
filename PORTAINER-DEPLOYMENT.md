# PORTAINER STACK DEPLOYMENT GUIDE
# Gästebuch-System für NAS (192.168.2.12)

## 🚀 DEPLOYMENT SCHRITTE:

### 1. Stack in Portainer erstellen:
- Name: `guestbook-production`
- Repository: Keine (Custom Template)
- Build method: Repository
- Compose file: `docker-compose.portainer-amd64.yml`

### 2. Environment Variables:
```env
DB_ROOT_PASSWORD=Kx9mP2vR8nQ5wE7tY3uI6oL1sA4hG9jB
DB_NAME=guestbook
DB_USER=guestuser
DB_PASSWORD=whHBJveMvwjs5a6p
JWT_SECRET_KEY=DeRBC3FDeY8d9nw9WMBwNJ0LpVyvB5ty607r2PHdmQBpqn
ADMIN_USERNAME=admin
ADMIN_EMAIL=support@dcng.de
ADMIN_PASSWORD=admin123
BACKEND_PORT=8000
FRONTEND_PORT=3000
REACT_APP_API_URL=http://192.168.2.12:8000
```

### 3. Container Images:
- Backend: `ghcr.io/baronblk/guestbook-project/backend:latest`
- Frontend: `ghcr.io/baronblk/guestbook-project/frontend:latest`
- Database: `mariadb:11`

### 4. Port Mapping:
- Frontend: `http://192.168.2.12:3000`
- Backend API: `http://192.168.2.12:8000`
- Admin Panel: `http://192.168.2.12:3000/admin`

### 5. Login-Daten:
- **Admin Username:** admin
- **Admin Password:** admin123
- **Admin Email:** support@dcng.de

### 6. Features:
✅ Session Management mit Timer
✅ File Upload für Reviews
✅ Admin Panel für Management
✅ Responsive Design
✅ Health Checks integriert
✅ Resource Limits für NAS-Performance

### 7. Troubleshooting:
- Container Logs in Portainer prüfen
- Health Status der Services überwachen
- Database Connectivity testen
- CORS Settings bei Netzwerkproblemen

---
**Ready to deploy!** 🎯
