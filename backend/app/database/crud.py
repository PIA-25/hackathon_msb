from typing import Optional, List
from . import models
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import logging

logger = logging.getLogger(__name__)

"""
Funktioner för att interagera med databasen för FRONTEND, GAME-ENGINE och AI
"""


def create_user(db: Session, firstname: str, lastname: str, age: int, krigsberedd: Optional[bool] = None) -> Optional[models.User]:
    """
    Skapar en ny användare i databasen.
    
    Args:
        db: Databassession
        firstname: Förnamn
        lastname: Efternamn
        age: Ålder
        krigsberedd: Om användaren är krigsberedd (optional)
    
    Returns:
        User-objekt om framgångsrikt, None vid fel
    
    Raises:
        SQLAlchemyError: Vid databasfel
    """
    try:
        user = models.User(
            firstname=firstname,
            lastname=lastname,
            age=age,
            krigsberedd=krigsberedd
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        logger.info(f"Created user: {user.user_id} - {firstname} {lastname}")
        return user
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error creating user: {e}")
        raise

def save_user_choice(db: Session, user_id: int, level_id: int, scenario_id: int, choice_id: int) -> Optional[models.UserChoice]:
    """
    Sparar en användares val i databasen.
    
    Args:
        db: Databassession
        user_id: Användarens ID
        level_id: Nivå-ID
        scenario_id: Scenario-ID
        choice_id: Val-ID
    
    Returns:
        UserChoice-objekt om framgångsrikt, None vid fel
    """
    try:
        user_choice = models.UserChoice(
            user_id=user_id,
            level_id=level_id,
            scenario_id=scenario_id,
            choice_id=choice_id
        )
        db.add(user_choice)
        db.commit()
        db.refresh(user_choice)
        logger.info(f"Saved user choice: user_id={user_id}, choice_id={choice_id}")
        return user_choice
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error saving user choice: {e}")
        raise


def get_scenario(db: Session, scenario_id: int) -> Optional[models.Scenario]:
    """Hämtar ett scenario baserat på ID."""
    try:
        return db.query(models.Scenario).filter(models.Scenario.scenario_id == scenario_id).first()
    except SQLAlchemyError as e:
        logger.error(f"Error getting scenario {scenario_id}: {e}")
        raise


def get_choice_options(db: Session, scenario_id: int, is_good: Optional[bool] = None) -> List[models.ChoiceOption]:
    """
    Hämtar alla alternativ för ett specifikt scenario.
    
    Args:
        db: Databassession
        scenario_id: Scenario-ID
        is_good: Om None, hämtar alla val. Om True, hämtar bara bra val. Om False, hämtar bara dåliga val.
    
    Returns:
        Lista med ChoiceOption-objekt
    """
    try:
        query = db.query(models.ChoiceOption).filter(models.ChoiceOption.scenario_id == scenario_id)
        if is_good is not None:
            query = query.filter(models.ChoiceOption.is_good == is_good)
        return query.all()
    except SQLAlchemyError as e:
        logger.error(f"Error getting choice options for scenario {scenario_id}: {e}")
        raise


def get_level(db: Session, level_id: int) -> Optional[models.Level]:
    """Hämtar en level baserat på ID."""
    try:
        return db.query(models.Level).filter(models.Level.level_id == level_id).first()
    except SQLAlchemyError as e:
        logger.error(f"Error getting level {level_id}: {e}")
        raise


def get_user(db: Session, user_id: int) -> Optional[models.User]:
    """Hämtar en användare baserat på ID."""
    try:
        return db.query(models.User).filter(models.User.user_id == user_id).first()
    except SQLAlchemyError as e:
        logger.error(f"Error getting user {user_id}: {e}")
        raise


def get_all_attributes(db: Session) -> List[models.Attribute]:
    """Hämtar alla attribut från databasen."""
    try:
        return db.query(models.Attribute).all()
    except SQLAlchemyError as e:
        logger.error(f"Error getting all attributes: {e}")
        raise


def get_attribute(db: Session, attribute_id: int) -> Optional[models.Attribute]:
    """Hämtar ett attribut baserat på ID."""
    try:
        return db.query(models.Attribute).filter(models.Attribute.attribute_id == attribute_id).first()
    except SQLAlchemyError as e:
        logger.error(f"Error getting attribute {attribute_id}: {e}")
        raise


def create_attribute(db: Session, name: str, description: Optional[str] = None) -> Optional[models.Attribute]:
    """Skapar ett nytt attribut i databasen."""
    try:
        attribute = models.Attribute(
            name=name,
            description=description
        )
        db.add(attribute)
        db.commit()
        db.refresh(attribute)
        logger.info(f"Created attribute: {attribute.attribute_id} - {name}")
        return attribute
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error creating attribute: {e}")
        raise


def update_user_attribute_score(db: Session, user_id: int, attribute_id: int, score_change: int) -> None:
    """
    Uppdaterar en användares attribut-poäng. Skapar relationen om den inte finns.
    
    Args:
        db: Databassession
        user_id: Användarens ID
        attribute_id: Attribut-ID
        score_change: Poängförändring (kan vara positiv eller negativ)
    
    Raises:
        SQLAlchemyError: Vid databasfel
    """
    from sqlalchemy import select, update, insert
    
    try:
        # Hämta användare och attribut för att säkerställa att de finns
        user = db.query(models.User).filter(models.User.user_id == user_id).first()
        attribute = db.query(models.Attribute).filter(models.Attribute.attribute_id == attribute_id).first()
        
        if not user:
            raise ValueError(f"User {user_id} not found")
        if not attribute:
            raise ValueError(f"Attribute {attribute_id} not found")
        
        # Kontrollera om relationen redan finns
        existing = db.execute(
            select(models.user_attributes.c.score).where(
                models.user_attributes.c.user_id == user_id,
                models.user_attributes.c.attribute_id == attribute_id
            )
        ).first()
        
        if existing:
            # Uppdatera befintlig poäng
            new_score = existing[0] + score_change
            db.execute(
                update(models.user_attributes)
                .where(
                    models.user_attributes.c.user_id == user_id,
                    models.user_attributes.c.attribute_id == attribute_id
                )
                .values(score=new_score)
            )
        else:
            # Skapa ny relation med startpoäng
            db.execute(
                insert(models.user_attributes).values(
                    user_id=user_id,
                    attribute_id=attribute_id,
                    score=score_change
                )
            )
        db.commit()
        logger.info(f"Updated user {user_id} attribute {attribute_id} score by {score_change}")
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error updating user attribute score: {e}")
        raise


def get_user_attributes(db: Session, user_id: int) -> List[dict]:
    """
    Hämtar alla attribut och deras poäng för en specifik användare.
    
    Args:
        db: Databassession
        user_id: Användarens ID
    
    Returns:
        Lista med dictionaries innehållande attributinformation och poäng
    """
    from sqlalchemy import func
    
    try:
        # Hämta alla attribut med LEFT JOIN för att få poäng om den finns
        result = db.query(
            models.Attribute.attribute_id,
            models.Attribute.name,
            models.Attribute.description,
            func.coalesce(models.user_attributes.c.score, 0).label('score')
        ).outerjoin(
            models.user_attributes,
            (models.user_attributes.c.attribute_id == models.Attribute.attribute_id) &
            (models.user_attributes.c.user_id == user_id)
        ).order_by(
            func.coalesce(models.user_attributes.c.score, 0).desc()
        ).all()
        
        return [
            {
                "attribute_id": row.attribute_id,
                "name": row.name,
                "description": row.description,
                "score": row.score
            }
            for row in result
        ]
    except SQLAlchemyError as e:
        logger.error(f"Error getting user attributes for user {user_id}: {e}")
        raise


def get_choice_attributes(db: Session, choice_id: int) -> List[dict]:
    """
    Hämtar alla attribut som påverkas av ett specifikt val.
    
    Args:
        db: Databassession
        choice_id: Val-ID
    
    Returns:
        Lista med dictionaries innehållande attributinformation och poängförändring
    """
    try:
        # Hämta valet för att använda relationship
        choice = db.query(models.ChoiceOption).filter(models.ChoiceOption.choice_id == choice_id).first()
        if not choice:
            return []
        
        # Använd ORM join för att hämta attribut med score_change
        result = db.query(
            models.Attribute.attribute_id,
            models.Attribute.name,
            models.choice_attributes.c.score_change
        ).join(
            models.choice_attributes,
            models.choice_attributes.c.attribute_id == models.Attribute.attribute_id
        ).filter(
            models.choice_attributes.c.choice_id == choice_id
        ).all()
        
        return [
            {
                "attribute_id": row.attribute_id,
                "name": row.name,
                "score_change": row.score_change
            }
            for row in result
        ]
    except SQLAlchemyError as e:
        logger.error(f"Error getting choice attributes for choice {choice_id}: {e}")
        raise


def link_choice_to_attribute(db: Session, choice_id: int, attribute_id: int, score_change: int) -> None:
    """
    Länkar ett val till ett attribut med en specifik poängförändring.
    Skapar länken om den inte finns, uppdaterar om den redan finns.
    
    Args:
        db: Databassession
        choice_id: Val-ID
        attribute_id: Attribut-ID
        score_change: Poängförändring
    
    Raises:
        SQLAlchemyError: Vid databasfel
    """
    from sqlalchemy import select, update, insert
    
    try:
        # Kontrollera om länken redan finns
        existing = db.execute(
            select(models.choice_attributes).where(
                models.choice_attributes.c.choice_id == choice_id,
                models.choice_attributes.c.attribute_id == attribute_id
            )
        ).first()
        
        if not existing:
            # Skapa ny länk
            db.execute(
                insert(models.choice_attributes).values(
                    choice_id=choice_id,
                    attribute_id=attribute_id,
                    score_change=score_change
                )
            )
        else:
            # Uppdatera befintlig länk
            db.execute(
                update(models.choice_attributes)
                .where(
                    models.choice_attributes.c.choice_id == choice_id,
                    models.choice_attributes.c.attribute_id == attribute_id
                )
                .values(score_change=score_change)
            )
        db.commit()
        logger.info(f"Linked choice {choice_id} to attribute {attribute_id} with score change {score_change}")
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error linking choice to attribute: {e}")
        raise


def save_user_choice_and_update_attributes(db: Session, user_id: int, level_id: int, scenario_id: int, choice_id: int) -> Optional[models.UserChoice]:
    """
    Sparar en användares val och uppdaterar deras attribut-poäng baserat på valet.
    Denna funktion använder en transaktion för att säkerställa dataintegritet.
    
    Args:
        db: Databassession
        user_id: Användarens ID
        level_id: Nivå-ID
        scenario_id: Scenario-ID
        choice_id: Val-ID
    
    Returns:
        UserChoice-objekt om framgångsrikt, None vid fel
    
    Raises:
        SQLAlchemyError: Vid databasfel (rollback sker automatiskt)
    """
    try:
        # Spara valet
        user_choice = save_user_choice(db, user_id, level_id, scenario_id, choice_id)
        
        # Hämta vilka attribut som påverkas av detta val
        choice_attrs = get_choice_attributes(db, choice_id)
        
        # Uppdatera användarens attribut-poäng
        for attr in choice_attrs:
            update_user_attribute_score(db, user_id, attr["attribute_id"], attr["score_change"])
        
        logger.info(f"Saved user choice and updated attributes for user {user_id}, choice {choice_id}")
        return user_choice
    except SQLAlchemyError as e:
        # Transaktionen kommer att rollbackas automatiskt om något fel uppstår
        logger.error(f"Error saving user choice and updating attributes: {e}")
        raise
