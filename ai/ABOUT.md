# AI Team — ABOUT

## Purpose
This folder contains all AI-related code and prompt engineering for the project.  
The AI team is responsible for:
- Prompt design & refinement  
- Integrating LLMs (ChatGPT, etc.)  
- NPC dialogue systems  
- AI-driven game mechanics  
- Data preprocessing & tooling  
- Logic for in-game AI behaviors  

## Where AI Developers Work
- **Main working branch:** `ai`  
- **Feature branches:** `feature/<name>/<task>`  

### Example
```
feature/sara/improve-npc-dialogue
```

## Workflow

### 1. Checkout ai branch
```bash
git checkout ai
git pull
```

### 2. Create a feature branch
```bash
git checkout -b feature/<name>/<task>
```

### 3. Make changes and commit (signed)
```bash
git add .
git commit -S -m "feat(ai): <message>"
```

### 4. Push branch
```bash
git push -u origin feature/<name>/<task>
```

### 5. Open PR into `develop`
Use GitHub → “Compare & pull request”

## Documentation
See the full onboarding guide here:  
[../docs/ONBOARDING.md](../docs/ONBOARDING.md)
