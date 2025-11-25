# backend/app/database/database.py

## Beskrivning
Databaskonfiguration och session-hantering för SQLAlchemy ORM. Denna modul sätter upp anslutningen till PostgreSQL-databasen och tillhandahåller funktioner för att skapa databassessioner.

## Komponenter

### DATABASE_URL
Anslutningssträng för PostgreSQL-databasen. **VIKTIGT:** Använd en `.env`-fil för att lagra användarnamn och lösenord istället för att hårdkoda dem i koden.

### engine
SQLAlchemy engine som hanterar databasanslutningen. `echo=True` loggar alla SQL-frågor till konsolen (användbart för debugging).

### SessionLocal
Session-fabrik för att skapa databassessioner med följande inställningar:
- `autocommit=False` - Ändringar kräver explicit commit
- `autoflush=False` - Flush-operationer måste anropas explicit

### Base
Basklass för deklarativa modeller. Alla databasmodeller bör ärva från denna Base.

## Funktioner

### `get_db()`
Generatorfunktion för att få en databassession. Säkerställer att sessionen stängs korrekt efter användning.

**Användning:**
```python
from backend.app.database.database import get_db

for db in get_db():
    # Använd db här
    user = db.query(models.User).first()
    break  # Sessionen stängs automatiskt efter loop
```

### `init_db()`
Skapar alla tabeller i databasen. Används för att initialisera databasen första gången.

**Användning:**
```python
from backend.app.database.database import init_db

init_db()  # Skapar alla tabeller
```

## Säkerhet
⚠️ **VIKTIGT:** 
- Använd en `.env`-fil för att lagra `DATABASE_URL` med känslig information
- Lägg aldrig in lösenord eller användarnamn direkt i koden
- Lägg till `.env` i `.gitignore` för att undvika att pusha känslig data till GitHub

## Exempel på .env-fil
```
DATABASE_URL=postgresql://användarnamn:lösenord@localhost:5432/databasnamn
```

## Relaterade filer
- `models.py` - Databasmodeller som använder Base
- `crud.py` - CRUD-operationer som använder SessionLocal

