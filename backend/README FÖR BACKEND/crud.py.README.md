# backend/app/database/crud.py

## Beskrivning
CRUD-operationer (Create, Read, Update, Delete) för databasinteraktioner. Denna modul innehåller funktioner för att interagera med databasen för FRONTEND, GAME-ENGINE och AI.

## Funktioner

### Användare (Users)
- `create_user()` - Skapar en ny användare
- `get_user()` - Hämtar en användare baserat på ID

### Scenarios och Val
- `get_scenario()` - Hämtar ett scenario baserat på ID
- `get_choice_options()` - Hämtar alla alternativ för ett scenario
- `save_user_choice()` - Sparar en användares val
- `save_user_choice_and_update_attributes()` - Sparar val och uppdaterar attribut-poäng automatiskt

### Nivåer (Levels)
- `get_level()` - Hämtar en nivå baserat på ID

### Attribut (Attributes)
- `get_all_attributes()` - Hämtar alla attribut
- `get_attribute()` - Hämtar ett attribut baserat på ID
- `create_attribute()` - Skapar ett nytt attribut
- `get_user_attributes()` - Hämtar alla attribut och poäng för en användare
- `update_user_attribute_score()` - Uppdaterar en användares attribut-poäng
- `get_choice_attributes()` - Hämtar attribut som påverkas av ett val
- `link_choice_to_attribute()` - Länkar ett val till ett attribut med poängförändring

## Användning

```python
from backend.app.database import crud
from backend.app.database.database import get_db

# Hämta databassession
db = next(get_db())

# Skapa användare
user = crud.create_user(db, firstname="Erik", lastname="Andersson", age=25, krigsberedd=True)

# Hämta scenario
scenario = crud.get_scenario(db, scenario_id=1)

# Hämta valalternativ
choices = crud.get_choice_options(db, scenario_id=1)

# Spara val och uppdatera attribut
user_choice = crud.save_user_choice_and_update_attributes(
    db, 
    user_id=1, 
    level_id=1, 
    scenario_id=1, 
    choice_id=2
)

# Hämta användarens attribut
attributes = crud.get_user_attributes(db, user_id=1)
```

## Felhantering
Alla funktioner använder try-except för att hantera SQLAlchemy-fel och loggar fel med Python's logging-modul. Vid fel sker automatiskt rollback av transaktioner.

## Logging
Modulen använder Python's logging för att logga:
- Skapade objekt
- Fel vid databasoperationer
- Uppdateringar av attribut-poäng

## Relaterade filer
- `models.py` - Databasmodeller som används av CRUD-funktionerna
- `database.py` - Databaskonfiguration och session-hantering

