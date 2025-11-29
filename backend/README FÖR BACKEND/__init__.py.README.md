# backend/app/database/__init__.py

## Beskrivning
Init-fil för `database`-modulen. Säkerställer att databasmoduler kan importeras korrekt.

## Syfte
- Gör databasmodulen tillgänglig för import
- Tillåter import av modeller, CRUD-operationer och databaskonfiguration

## Användning
```python
from backend.app.database import models
from backend.app.database import crud
from backend.app.database import database
```

## Relaterade filer
- `models.py` - Databasmodeller
- `crud.py` - CRUD-operationer
- `database.py` - Databaskonfiguration

