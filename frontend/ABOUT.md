# Frontend Team — ABOUT

## Purpose
This folder contains all frontend-related code for the user interface.  
The frontend team is responsible for:
- UI development  
- Component creation  
- API integration  
- Styling and layout  
- User experience improvements  

## Where Frontend Developers Work
- **Main working branch:** `frontend`  
- **Feature branches:** `feature/<name>/<task>`  

### Example
```
feature/lisa/create-homepage
```

## Workflow

### 1. Checkout frontend branch
```bash
git checkout frontend
git pull
```

### 2. Create a feature branch
```bash
git checkout -b feature/<name>/<task>
```

### 3. Make changes and commit (signed)
```bash
git add .
git commit -S -m "feat(frontend): <message>"
```

### 4. Push branch
```bash
git push -u origin feature/<name>/<task>
```

### 5. Open PR into `develop`
Use GitHub → “Compare & pull request”.

## Documentation
See the full onboarding guide:  
[../docs/ONBOARDING.md](../docs/ONBOARDING.md)
