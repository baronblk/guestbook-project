# Contributing Guide

Vielen Dank für dein Interesse am Guestbook-Projekt! 🎉

## 🤝 Wie du beitragen kannst

### 🐛 Bug Reports
- Verwende das [Bug Report Template](.github/ISSUE_TEMPLATE/bug_report.md)
- Beschreibe das Problem detailliert
- Füge Screenshots bei, wenn möglich
- Teste in verschiedenen Browsern

### ✨ Feature Requests  
- Verwende das [Feature Request Template](.github/ISSUE_TEMPLATE/feature_request.md)
- Erkläre den Use Case klar
- Diskutiere Alternativen

### 💻 Code Contributions

#### Setup
```bash
git clone https://github.com/baronblk/guestbook-project.git
cd guestbook-project
docker-compose up --build
```

#### Workflow
1. **Fork** das Repository
2. **Branch** erstellen: `git checkout -b feature/awesome-feature`
3. **Entwickeln** und testen
4. **Commit**: `git commit -m 'Add awesome feature'`
5. **Push**: `git push origin feature/awesome-feature`
6. **Pull Request** erstellen

#### Code Standards
- **Backend**: Python Black + Flake8
- **Frontend**: ESLint + Prettier
- **Commits**: [Conventional Commits](https://conventionalcommits.org/)
- **Tests**: Mindestens 80% Coverage

#### Commit Message Format
```
type(scope): description

[optional body]

[optional footer]
```

**Types**: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

**Beispiele**:
- `feat(frontend): add comment moderation panel`
- `fix(backend): resolve JWT token expiration issue`
- `docs(readme): update installation instructions`

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
pytest --cov=app tests/
```

### Frontend Tests
```bash
cd frontend
npm test
npm run test:coverage
```

### E2E Tests
```bash
npm run test:e2e
```

## 📋 Pull Request Checklist

- [ ] Tests hinzugefügt/aktualisiert
- [ ] Dokumentation aktualisiert
- [ ] CHANGELOG.md aktualisiert
- [ ] Code Style befolgt
- [ ] Keine Breaking Changes (oder dokumentiert)
- [ ] Screenshots bei UI-Änderungen

## 🔄 Review Process

1. **Automatische Checks** müssen grün sein
2. **Code Review** von mindestens einem Maintainer
3. **Testing** in verschiedenen Umgebungen
4. **Merge** nach Approval

## 🎯 Development Guidelines

### Frontend
- **React Hooks** bevorzugen
- **TypeScript** für Type Safety
- **TailwindCSS** für Styling
- **Zustand** für State Management

### Backend
- **FastAPI** Best Practices
- **SQLAlchemy** für Database
- **Pydantic** für Validation
- **JWT** für Authentication

### Docker
- **Multi-stage** Builds
- **Health Checks** einbauen
- **Security** Best Practices
- **Multi-platform** Support

## 🏷️ Labels

- `bug` - Etwas funktioniert nicht
- `enhancement` - Neue Features
- `documentation` - Verbesserungen der Dokumentation
- `good first issue` - Gut für Newcomer
- `help wanted` - Extra Aufmerksamkeit gewünscht
- `priority-high` - Hohe Priorität
- `priority-low` - Niedrige Priorität

## 💬 Communication

- **Issues** für Bugs und Features
- **Discussions** für allgemeine Fragen
- **Pull Requests** für Code-Änderungen

## 🙏 Anerkennung

Alle Beiträge werden in der [Contributors](https://github.com/baronblk/guestbook-project/graphs/contributors) Seite anerkannt.

---

**Vielen Dank für deine Hilfe beim Verbessern des Guestbook-Systems! 🚀**
