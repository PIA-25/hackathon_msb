# backend/app/database/models.py

## Beskrivning
SQLAlchemy ORM-modeller för databasen. Denna fil definierar alla tabeller och deras relationer i databasen.

## Tabeller

### User (users)
Användartabell som lagrar information om spelare.

**Kolumner:**
- `user_id` (Integer, Primary Key) - Unikt ID för användaren
- `firstname` (String) - Förnamn
- `lastname` (String) - Efternamn
- `age` (Integer) - Ålder (18-29 år)
- `krigsberedd` (Boolean, nullable) - Om användaren är krigsberedd
- `created_at` (DateTime) - Skapad datum/tid

**Relationer:**
- Har många `UserChoice`
- Har många `Attribute` via `user_attributes` (många-till-många)

### Level (levels)
Nivåtabell som representerar olika nivåer i spelet.

**Kolumner:**
- `level_id` (Integer, Primary Key) - Unikt ID för nivån
- `level_number` (Integer) - Nivånummer
- `title` (String) - Titel för nivån

**Relationer:**
- Har många `Scenario`
- Har många `UserChoice`

### Scenario (scenarios)
Scenariotabell som innehåller olika scenarion för varje nivå.

**Kolumner:**
- `scenario_id` (Integer, Primary Key) - Unikt ID för scenariot
- `level_id` (Integer, Foreign Key) - Referens till Level
- `scenario_text` (Text) - Beskrivning av scenariot

**Relationer:**
- Tillhör en `Level`
- Har många `ChoiceOption`
- Har många `UserChoice`

### ChoiceOption (choice_options)
Valalternativ för varje scenario.

**Kolumner:**
- `choice_id` (Integer, Primary Key) - Unikt ID för valet
- `scenario_id` (Integer, Foreign Key) - Referens till Scenario
- `option_text` (Text) - Texten som spelaren ser
- `outcome_text` (Text) - Feedback efter valet
- `is_good` (Boolean, nullable) - true = bra val, false = dåligt val, NULL = neutralt

**Relationer:**
- Tillhör ett `Scenario`
- Har många `UserChoice`
- Har många `Attribute` via `choice_attributes` (många-till-många)

### UserChoice (user_choices)
Tabell som lagrar användarens val.

**Kolumner:**
- `user_choice_id` (Integer, Primary Key) - Unikt ID för valet
- `user_id` (Integer, Foreign Key) - Referens till User
- `level_id` (Integer, Foreign Key) - Referens till Level
- `scenario_id` (Integer, Foreign Key) - Referens till Scenario
- `choice_id` (Integer, Foreign Key) - Referens till ChoiceOption
- `chosen_at` (DateTime) - När valet gjordes

**Relationer:**
- Tillhör en `User`
- Tillhör en `Level`
- Tillhör ett `Scenario`
- Tillhör ett `ChoiceOption`

### Attribute (attributes)
Attribut som användare kan ha (t.ex. "loyal", "taktisk", "ödmjuk").

**Kolumner:**
- `attribute_id` (Integer, Primary Key) - Unikt ID för attributet
- `name` (String, unique) - Namn på attributet
- `description` (Text, nullable) - Beskrivning av attributet

**Relationer:**
- Har många `User` via `user_attributes` (många-till-många)
- Har många `ChoiceOption` via `choice_attributes` (många-till-många)

## Kopplingstabeller

### user_attributes
Kopplingstabell mellan Users och Attributes.

**Kolumner:**
- `user_id` (Integer, Foreign Key, Primary Key)
- `attribute_id` (Integer, Foreign Key, Primary Key)
- `score` (Integer, default=0) - Poäng för detta attribut för denna användare

### choice_attributes
Kopplingstabell mellan ChoiceOptions och Attributes.

**Kolumner:**
- `choice_id` (Integer, Foreign Key, Primary Key)
- `attribute_id` (Integer, Foreign Key, Primary Key)
- `score_change` (Integer) - Hur mycket detta val påverkar attributet (+ eller -)

## Användning

```python
from backend.app.database import models
from backend.app.database.database import SessionLocal

# Skapa session
db = SessionLocal()

# Skapa ny användare
user = models.User(
    firstname="Erik",
    lastname="Andersson",
    age=25,
    krigsberedd=True
)
db.add(user)
db.commit()

# Hämta användare med relationer
user = db.query(models.User).filter(models.User.user_id == 1).first()
user_choices = user.user_choices  # Hämta alla val
attributes = user.attributes  # Hämta alla attribut
```

## Relaterade filer
- `database.py` - Base-klass och databaskonfiguration
- `crud.py` - CRUD-operationer som använder dessa modeller

