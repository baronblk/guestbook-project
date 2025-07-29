# 🔧 Development Guide

## 🚀 Setup für Entwicklung

### Voraussetzungen
- Node.js 18+
- Python 3.9+
- Docker & Docker Compose
- Git

### 1. Entwicklungsumgebung einrichten

```bash
# Repository klonen
git clone https://github.com/baronblk/guestbook-project.git
cd guestbook-project

# Backend Setup
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
pip install -r requirements.txt

# Frontend Setup
cd ../frontend
npm install
```

### 2. Development Server starten

**Option A: Separate Services**
```bash
# Terminal 1: Database
docker-compose up db

# Terminal 2: Backend
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000

# Terminal 3: Frontend
cd frontend
npm start
```

**Option B: Docker Compose (Vollständig)**
```bash
docker-compose up --build
```

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
pytest --cov=app tests/  # Mit Coverage
```

### Frontend Tests
```bash
cd frontend
npm test
npm run test:coverage
```

### E2E Tests
```bash
# Playwright oder Cypress Setup
npm run test:e2e
```

## 🎨 Code Style

### Backend (Python)
```bash
# Code Formatting
black backend/
isort backend/

# Linting
flake8 backend/
mypy backend/
```

### Frontend (TypeScript/React)
```bash
cd frontend
npm run lint
npm run lint:fix
npm run type-check
```

## 📦 Build Process

### Development Build
```bash
# Frontend Development Build
cd frontend
npm run build:dev

# Backend Development
cd backend
python -m app.main
```

### Production Build
```bash
# Docker Multi-Stage Build
docker build -f Dockerfile.combined -t guestbook:latest .

# Multi-Platform Build
docker buildx build --platform linux/amd64,linux/arm64 \
  -t ghcr.io/baronblk/guestbook-project/combined:latest \
  -f Dockerfile.combined --push .
```

## 🗃️ Datenbank

### Schema Änderungen
```bash
# Neue Migration erstellen
cd backend
alembic revision --autogenerate -m "Add new feature"

# Migration ausführen
alembic upgrade head
```

### Test Daten
```bash
# Test Reviews erstellen
python scripts/create_test_data.py

# Admin User erstellen
python backend/create_admin.py
```

## 🔍 Debugging

### Backend Debugging
```python
# In main.py
import uvicorn
uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True, log_level="debug")
```

### Frontend Debugging
```javascript
// React Developer Tools
// Redux DevTools Extension
// Browser Developer Console
```

### Docker Debugging
```bash
# Container Logs
docker-compose logs -f app
docker-compose logs -f db

# In Container ausführen
docker-compose exec app bash
docker-compose exec db mysql -u root -p
```

## 🚀 Deployment

### Staging Deployment
```bash
# Staging Image builden
docker build -f Dockerfile.combined -t guestbook:staging .

# Staging starten
docker-compose -f docker-compose.staging.yml up -d
```

### Production Deployment
```bash
# Production Image pushen
docker buildx build --platform linux/amd64,linux/arm64 \
  -t ghcr.io/baronblk/guestbook-project/combined:latest \
  -f Dockerfile.combined --push .

# Auf Server deployen
ssh user@192.168.2.12
docker-compose -f docker-compose.combined.yml pull
docker-compose -f docker-compose.combined.yml up -d
```

## 📊 Monitoring

### Health Checks
- **Backend**: http://localhost:8000/health
- **Frontend**: http://localhost:3000 (Status Code 200)
- **Database**: Docker Health Check

### Logs
```bash
# Application Logs
docker-compose logs -f app

# Database Logs  
docker-compose logs -f db

# Nginx Logs
docker-compose exec app tail -f /var/log/nginx/access.log
```

## 🔧 Troubleshooting

### Häufige Probleme

**Port bereits belegt:**
```bash
lsof -ti:3000 | xargs kill -9  # Frontend Port
lsof -ti:8000 | xargs kill -9  # Backend Port
```

**Docker Image Probleme:**
```bash
docker system prune -a
docker-compose build --no-cache
```

**Database Connection:**
```bash
# MariaDB direkt testen
docker-compose exec db mysql -u guestuser -p guestbook
```

### Performance Optimization

**Backend:**
- Connection Pooling prüfen
- Query Optimization
- Caching implementieren

**Frontend:**
- Bundle Size analyzieren: `npm run analyze`
- Lazy Loading für Components
- Image Optimization

---

*Weitere Entwickler-Ressourcen im `docs/` Verzeichnis*
