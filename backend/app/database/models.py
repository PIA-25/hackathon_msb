from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean, func, Table
from sqlalchemy.orm import relationship
from .database import Base

if TYPE_CHECKING:
    # För type hints vid circular imports
    pass

"""
Här definierar vi de olika tabellerna i databasen.
Alla modeller ärver från Base och använder SQLAlchemy ORM.
"""

# Kopplingstabell för  relation mellan Users och Attributes
user_attributes = Table(
    'user_attributes',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.user_id'), primary_key=True),
    Column('attribute_id', Integer, ForeignKey('attributes.attribute_id'), primary_key=True),
    Column('score', Integer, default=0)  # Poäng för detta attribut för denna användare
)

# Kopplingstabell för  relation mellan ChoiceOptions och Attributes
# Varje val kan påverka flera attribut med olika poäng
choice_attributes = Table(
    'choice_attributes',
    Base.metadata,
    Column('choice_id', Integer, ForeignKey('choice_options.choice_id'), primary_key=True),
    Column('attribute_id', Integer, ForeignKey('attributes.attribute_id'), primary_key=True),
    Column('score_change', Integer, nullable=False)  # Hur mycket detta val påverkar attributet (+ eller -)
)


"""Tabell Users"""
class User(Base):
    __tablename__ = "users"
    
    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    firstname = Column(String(50), index=True)
    lastname = Column(String(50), index=True)
    age = Column(Integer, index=True)  # 18–29 år
    krigsberedd = Column(Boolean, nullable=True)  # true = ja, false = nej
    created_at = Column(DateTime, server_default=func.now())

    user_choices: "List[UserChoice]" = relationship("UserChoice", back_populates="user")
    attributes: "List[Attribute]" = relationship("Attribute", secondary=user_attributes, back_populates="users")


"""Tabell Levels"""
class Level(Base):
    __tablename__ = "levels"
    
    level_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    level_number = Column(Integer, nullable=False)
    title = Column(String(100), nullable=True)

    scenarios: "List[Scenario]" = relationship("Scenario", back_populates="level")
    user_choices: "List[UserChoice]" = relationship("UserChoice", back_populates="level")


"""Tabell Scenarios"""
class Scenario(Base):
    __tablename__ = "scenarios"
    
    scenario_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    level_id = Column(Integer, ForeignKey("levels.level_id"), nullable=False)
    scenario_text = Column(Text, nullable=False)

    level: "Level" = relationship("Level", back_populates="scenarios")
    choice_options: "List[ChoiceOption]" = relationship("ChoiceOption", back_populates="scenario")
    user_choices: "List[UserChoice]" = relationship("UserChoice", back_populates="scenario")


"""Tabell Choice Options"""
class ChoiceOption(Base):
    __tablename__ = "choice_options"
    
    choice_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    scenario_id = Column(Integer, ForeignKey("scenarios.scenario_id"), nullable=False)
    option_text = Column(Text, nullable=False)  # valet spelaren ser
    outcome_text = Column(Text, nullable=False)  # feedback efter valet
    is_good = Column(Boolean, nullable=True)  # true = bra val, false = dåligt val, NULL = neutralt

    scenario: "Scenario" = relationship("Scenario", back_populates="choice_options")
    user_choices: "List[UserChoice]" = relationship("UserChoice", back_populates="choice_option")
    attributes: "List[Attribute]" = relationship("Attribute", secondary=choice_attributes, back_populates="choice_options")


"""Tabell User Choices"""
class UserChoice(Base):
    __tablename__ = "user_choices"
    
    user_choice_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    level_id = Column(Integer, ForeignKey("levels.level_id"), nullable=False)
    scenario_id = Column(Integer, ForeignKey("scenarios.scenario_id"), nullable=False)
    choice_id = Column(Integer, ForeignKey("choice_options.choice_id"), nullable=False)
    chosen_at = Column(DateTime, server_default=func.now())

    user: "User" = relationship("User", back_populates="user_choices")
    level: "Level" = relationship("Level", back_populates="user_choices")
    scenario: "Scenario" = relationship("Scenario", back_populates="user_choices")
    choice_option: "ChoiceOption" = relationship("ChoiceOption", back_populates="user_choices")


"""Tabell Attributes"""
class Attribute(Base):
    __tablename__ = "attributes"
    
    attribute_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)  # t.ex. "loyal", "taktisk", "ödmjuk"
    description = Column(Text, nullable=True)

    users: "List[User]" = relationship("User", secondary=user_attributes, back_populates="attributes")
    choice_options: "List[ChoiceOption]" = relationship("ChoiceOption", secondary=choice_attributes, back_populates="attributes")
