from sqlalchemy import Column, Integer, String,DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
"""Här definierar vi de olika tabellerna i databasen"""


"""Tabell Users"""
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer, index=True) #18–29 år
    created_at = Column(DateTime, default=DateTime.now)

    scenarios = relationship("Scenario", back_populates="user")
    responses = relationship("Response", back_populates="user")

"""Tabell scenarios"""
class scenario(Base):
    __tablename__ = "scenarios"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True) #Varje scenario är unik för varje användare.
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    options = relationship("Option", back_populates="scenario")

"""Tabell Options"""
class Option(Base):
    __tablename__ = "options"
    id = Column(Integer, primary_key=True, index=True)
    scenario_id = Column(Integer, ForeignKey("scenarios.id"))
    text = Column(String, nullable=False)

    # next_scenario_id = Column(Integer, nullable=True), vet ej om detta kommer behövas då scenariorna skapas on the fly

    scenario = relationship("Scenario", back_populates="options")
    responses = relationship("Response", back_populates="option")

"""Tabell Responses"""
class Response(Base):
    __tablename__ = "responses"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    scenario_id = Column(Integer, ForeignKey("scenarios.id"))
    option_id = Column(Integer, ForeignKey("options.id"))
    timestamp = Column(DateTime, default=DateTime.now)

    user = relationship("User", back_populates="responses")
    option = relationship("Option", back_populates="responses")