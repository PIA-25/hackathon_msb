# Backend Team — ABOUT

## Purpose
This folder contains all backend-related code for the project. The backend team is responsible for:
- API endpoints  
- Authentication & authorization  
- Database models & schemas  
- Backend services and logic  

## Where Backend Developers Work
- **Main working branch:** `backend`  
- **Feature branches:** `feature/<name>/<task>`  

### Example
```
feature/jane/add-login-endpoint
```

## Workflow

### 1. Checkout backend branch
```bash
git checkout backend
git pull
```

### 2. Create a feature branch
```bash
git checkout -b feature/<name>/<task>
```

### 3. Make changes and commit (signed)
```bash
git add .
git commit -S -m "feat(backend): <message>"
```

### 4. Push branch
```bash
git push -u origin feature/<name>/<task>
```

### 5. Open PR into `develop`
Use GitHub → “Compare & pull request”.

## Documentation
See the full onboarding guide here:  
[../docs/ONBOARDING.md](../docs/ONBOARDING.md)
