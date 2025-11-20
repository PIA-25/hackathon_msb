# Game Team — ABOUT

## Purpose
This folder contains all game-related code for the project.  
The game team is responsible for:
- Game engine logic  
- Player mechanics  
- World interactions  
- Game rules & systems  
- Internal gameplay architecture  

## Where Game Developers Work
- **Main working branch:** `game`  
- **Feature branches:** `feature/<name>/<task>`  

### Example
```
feature/max/add-player-movement
```

## Workflow

### 1. Checkout game branch
```bash
git checkout game
git pull
```

### 2. Create a feature branch
```bash
git checkout -b feature/<name>/<task>
```

### 3. Make changes and commit (signed)
```bash
git add .
git commit -S -m "feat(game): <message>"
```

### 4. Push the branch
```bash
git push -u origin feature/<name>/<task>
```

### 5. Open PR into `develop`
Use GitHub → “Compare & pull request”

## Documentation
See the full onboarding guide here:  
[../docs/ONBOARDING.md](../docs/ONBOARDING.md)
