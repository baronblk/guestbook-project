# Contributing zum Guestbook Projekt

Vielen Dank für dein Interesse, zu diesem Projekt beizutragen! 🎉

## Wie du beitragen kannst

### 🐛 Bug Reports
- Suche zuerst in den [Issues](../../issues), ob der Bug bereits gemeldet wurde
- Erstelle ein neues Issue mit dem "Bug Report" Template
- Beschreibe das Problem so detailliert wie möglich
- Füge Screenshots hinzu, falls hilfreich

### 💡 Feature Requests
- Suche zuerst in den [Issues](../../issues), ob das Feature bereits vorgeschlagen wurde
- Erstelle ein neues Issue mit dem "Feature Request" Template
- Erkläre, warum das Feature nützlich wäre
- Beschreibe die gewünschte Funktionalität

### 🔧 Code Contributions

#### Vorbereitung
1. **Fork** das Repository
2. **Clone** deinen Fork lokal
3. Erstelle einen neuen **Branch** für deine Änderungen:
   ```bash
   git checkout -b feature/deine-feature-beschreibung
   ```

#### Development Setup
```bash
# Repository klonen
git clone https://github.com/dein-username/guestbook-project.git
cd guestbook-project

# Development-Umgebung starten
docker-compose up --build

# Tests ausführen (falls vorhanden)
docker-compose exec backend pytest
docker-compose exec frontend npm test
```

#### Code-Standards
- **Python**: Befolge PEP 8, nutze Black für Formatierung
- **TypeScript/React**: Nutze Prettier und ESLint
- **Commits**: Nutze [Conventional Commits](https://www.conventionalcommits.org/)
  - `feat:` für neue Features
  - `fix:` für Bugfixes
  - `docs:` für Dokumentationsänderungen
  - `style:` für Code-Formatierung
  - `refactor:` für Code-Refactoring
  - `test:` für Tests
  - `chore:` für Maintenance-Tasks

#### Pull Request Process
1. **Aktualisiere** deinen Branch mit den neuesten Änderungen:
   ```bash
   git fetch upstream
   git rebase upstream/master
   ```
2. **Teste** deine Änderungen gründlich
3. **Committe** deine Änderungen mit aussagekräftigen Nachrichten
4. **Push** deinen Branch zu deinem Fork
5. **Erstelle** einen Pull Request mit:
   - Klare Beschreibung der Änderungen
   - Referenz zu related Issues (falls vorhanden)
   - Screenshots bei UI-Änderungen

## 📋 Development Guidelines

### Backend (FastAPI + Python)
- Nutze Type Hints für alle Funktionen
- Schreibe Docstrings für komplexe Funktionen
- Halte die API-Endpoints RESTful
- Validiere alle Eingaben mit Pydantic

### Frontend (React + TypeScript)
- Nutze funktionale Komponenten mit Hooks
- Implementiere TypeScript strikt (keine `any` Types)
- Komponenten sollten wiederverwendbar sein
- Nutze Zustand für State Management

### Database
- Nutze SQLAlchemy ORM
- Schreibe Migrations für Schema-Änderungen
- Beachte Performance bei Queries

## 🧪 Testing
- Schreibe Tests für neue Features
- Stelle sicher, dass alle Tests bestehen
- Teste manuelle Szenarien im Browser

## 📝 Dokumentation
- Aktualisiere das README.md bei API-Änderungen
- Dokumentiere neue Environment-Variablen
- Halte das CHANGELOG.md aktuell

## 🤝 Code of Conduct
- Sei respektvoll und konstruktiv
- Hilf anderen Contributoren
- Fokussiere dich auf das Problem, nicht die Person

## ❓ Fragen?
Bei Fragen erstelle ein Issue oder kontaktiere die Maintainer.

Vielen Dank für deinen Beitrag! 🚀
