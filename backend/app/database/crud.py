from . import models
from sqlalchemy.orm import Session
"""
Funktioner för att interagera med databasen för FRONTEND, GAME-ENGINE och AI
"""
def create_user(db: Session, firstname: str, lastname: str, age: int, krigsberedd: bool = None) -> models.User:
    """Skapar en ny användare i databasen."""
    user = models.User(
        firstname=firstname,
        lastname=lastname,
        age=age,
        krigsberedd=krigsberedd
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def save_user_choice(db: Session, user_id: int, level_id: int, scenario_id: int, choice_id: int) -> models.UserChoice:
    """Sparar en användares val i databasen."""
    user_choice = models.UserChoice(
        user_id=user_id,
        level_id=level_id,
        scenario_id=scenario_id,
        choice_id=choice_id
    )
    db.add(user_choice)
    db.commit()
    db.refresh(user_choice)
    return user_choice


def get_scenario(db: Session, scenario_id: int) -> models.Scenario:
    """Hämtar ett scenario baserat på ID."""
    return db.query(models.Scenario).filter(models.Scenario.scenario_id == scenario_id).first()


def get_choice_options(db: Session, scenario_id: int) -> list[models.ChoiceOption]:
    """Hämtar alla alternativ för ett specifikt scenario."""
    return db.query(models.ChoiceOption).filter(models.ChoiceOption.scenario_id == scenario_id).all()


def get_level(db: Session, level_id: int) -> models.Level:
    """Hämtar en level baserat på ID."""
    return db.query(models.Level).filter(models.Level.level_id == level_id).first()


def get_user(db: Session, user_id: int) -> models.User:
    """Hämtar en användare baserat på ID."""
    return db.query(models.User).filter(models.User.user_id == user_id).first()