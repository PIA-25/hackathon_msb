from . import models
from sqlalchemy.orm import Session
"""
Funktioner för att interagera med databasen för FRONTEND, GAME-ENGINE och AI
"""
def create_user(db: Session, name: str, age: int) -> int: # -> int: returnerar en integer
    """Skapar en ny användare i databasen."""
    user = models.User(name=name, age=age)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def save_response(user_id: int, scenario_id: int, option_id: int) -> int:
    """Sparar en användares val i databasen."""
    pass


def get_scenario(id: int) -> dict: # -> dict: returnerar en dictionary
    """Hämtar ett scenario baserat på ID."""
    pass


def get_options(scenario_id: int) -> list: # -> list: returnerar en lista
    """Hämtar alla alternativ för ett specifikt scenario."""
    pass

