from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean, func
from sqlalchemy.orm import relationship
from .database import Base
"""Här definierar vi de olika tabellerna i databasen"""


"""Tabell Users"""
class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    firstname = Column(String(50), index=True)
    lastname = Column(String(50), index=True)
    age = Column(Integer, index=True)  # 18–29 år
    krigsberedd = Column(Boolean)  # true = ja, false = nej
    created_at = Column(DateTime, server_default=func.now())

    user_choices = relationship("UserChoice", back_populates="user")


"""Tabell Levels"""
class Level(Base):
    __tablename__ = "levels"
    level_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    level_number = Column(Integer, nullable=False)
    title = Column(String(100))

    scenarios = relationship("Scenario", back_populates="level")
    user_choices = relationship("UserChoice", back_populates="level")


"""Tabell Scenarios"""
class Scenario(Base):
    __tablename__ = "scenarios"
    scenario_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    level_id = Column(Integer, ForeignKey("levels.level_id"), nullable=False)
    scenario_text = Column(Text, nullable=False)

    level = relationship("Level", back_populates="scenarios")
    choice_options = relationship("ChoiceOption", back_populates="scenario")
    user_choices = relationship("UserChoice", back_populates="scenario")


"""Tabell Choice Options"""
class ChoiceOption(Base):
    __tablename__ = "choice_options"
    choice_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    scenario_id = Column(Integer, ForeignKey("scenarios.scenario_id"), nullable=False)
    option_text = Column(Text, nullable=False)  # valet spelaren ser
    outcome_text = Column(Text, nullable=False)  # feedback efter valet

    scenario = relationship("Scenario", back_populates="choice_options")
    user_choices = relationship("UserChoice", back_populates="choice_option")


"""Tabell User Choices"""
class UserChoice(Base):
    __tablename__ = "user_choices"
    user_choice_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    level_id = Column(Integer, ForeignKey("levels.level_id"), nullable=False)
    scenario_id = Column(Integer, ForeignKey("scenarios.scenario_id"), nullable=False)
    choice_id = Column(Integer, ForeignKey("choice_options.choice_id"), nullable=False)
    chosen_at = Column(DateTime, server_default=func.now())

    user = relationship("User", back_populates="user_choices")
    level = relationship("Level", back_populates="user_choices")
    scenario = relationship("Scenario", back_populates="user_choices")
    choice_option = relationship("ChoiceOption", back_populates="user_choices")


"""Tabell Attributes"""
class Attribute(Base):
    __tablename__ = "attributes"
    attribute_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    description = Column(Text)
