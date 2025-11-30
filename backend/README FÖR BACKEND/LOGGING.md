# Logging Guide

## Översikt

Projektet använder Python's inbyggda `logging`-modul för att logga händelser och fel.

## Hur det fungerar

### Grundläggande setup

I varje modul skapas en logger så här:

```python
import logging

logger = logging.getLogger(__name__)
```

`__name__` är modulens namn, vilket gör att varje modul får sin egen logger.

### Log-nivåer

Logger har fem nivåer (från minst till mest allvarlig):

1. **DEBUG** - Detaljerad debug-information
2. **INFO** - Informativt meddelande (framgångsrika operationer)
3. **WARNING** - Varning - något oväntat hände
4. **ERROR** - Ett fel uppstod
5. **CRITICAL** - Kritiskt fel

### Användning i koden

I `crud.py` används två nivåer:

```python
# Logga framgångsrika operationer
logger.info(f"Created user: {user.user_id} - {firstname} {lastname}")

# Logga fel
logger.error(f"Error creating user: {e}")
```

## Vad loggas?

### INFO-meddelanden
- När användare skapas
- När val sparas
- När attribut skapas
- När attributpoäng uppdateras
- När val länkas till attribut

### ERROR-meddelanden
- När databasoperationer misslyckas
- När queries inte kan köras
- När transaktioner rollbackas

## Var ser jag loggarna?

Loggarna skrivs till konsolen när du kör applikationen.

### Exempel på loggutskrift

```
2024-01-15 10:30:45 - app.database.crud - INFO - Created user: 1 - Anna Andersson
2024-01-15 10:30:46 - app.database.crud - INFO - Saved user choice: user_id=1, choice_id=5
2024-01-15 10:30:47 - app.database.crud - ERROR - Error getting user 999: [felmeddelande]
```

## Konfigurera loggning

Loggning konfigureras i `main.py` (eller där applikationen startar):

```python
logging.basicConfig(
    level=logging.INFO,  # Visa INFO och högre nivåer
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### Ändra loggningsnivå

För mer detaljerad loggning (inklusive DEBUG):

```python
logging.basicConfig(level=logging.DEBUG)
```

För mindre loggning (bara ERROR och CRITICAL):

```python
logging.basicConfig(level=logging.ERROR)
```

## Tips

- **Utveckling**: Använd `logging.DEBUG` för att se allt
- **Produktion**: Använd `logging.INFO` eller `logging.WARNING` för att minska loggvolymen
- **Felsökning**: Leta efter ERROR-meddelanden för att hitta problem

## Ytterligare läsning

- [Python Logging Documentation](https://docs.python.org/3/library/logging.html)
- [Logging Best Practices](https://docs.python.org/3/howto/logging.html)

