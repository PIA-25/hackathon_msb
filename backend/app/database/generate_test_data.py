"""
Test Data Generator
===================
Generates large amounts of test data for the database to populate project statistics.
Run this script to fill the database with realistic test data.
"""

import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(project_root))

import random
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError
from sqlalchemy import select, insert, update

from backend.app.database.database import SessionLocal, init_db
from backend.app.database.models import (
    User, Attribute, Level, Scenario, ChoiceOption, UserChoice,
    user_attributes, choice_attributes
)

# Valid values from registration form
GENDERS = ['Man', 'Kvinna', 'Annat', 'Vill inte ange']
OCCUPATIONS = ['Ingenjör', 'Läkare', 'Lärare', 'Företagare', 'Konsult', 'Forskare', 'Annat']
LEADERSHIP_STYLES = ['Aggressiv', 'Defensiv', 'Diplomatisk', 'Balanserad']
PRIORITIES = ['Hjälpa andra', 'Fly/Överleva', 'Konfrontera hotet', 'Samla information']
TEAM_ROLES = ['Ledare', 'Lagspelare', 'Ensam varg', 'Stöttande']
RISK_TOLERANCES = ['Försiktig', 'Måttlig', 'Våghalsig']

# Swedish first names for realistic usernames
FIRST_NAMES = [
    'Erik', 'Anna', 'Lars', 'Maria', 'Anders', 'Karin', 'Johan', 'Emma',
    'Per', 'Sara', 'Mikael', 'Lisa', 'Daniel', 'Jenny', 'Fredrik', 'Sofia',
    'Magnus', 'Linda', 'Peter', 'Malin', 'Thomas', 'Camilla', 'Martin', 'Hanna',
    'Andreas', 'Elin', 'Marcus', 'Amanda', 'David', 'Frida', 'Niklas', 'Ida',
    'Stefan', 'Julia', 'Henrik', 'Elin', 'Jonas', 'Nina', 'Mattias', 'Therese'
]

# Attribute names for the game
ATTRIBUTE_NAMES = [
    ('Taktisk', 'Förmåga att planera och tänka strategiskt'),
    ('Lojalitet', 'Pålitlighet och trogenhet mot team och organisation'),
    ('Mod', 'Förmåga att agera under press och i farliga situationer'),
    ('Empati', 'Förmåga att förstå och känna med andra'),
    ('Beslutsamhet', 'Förmåga att fatta snabba och effektiva beslut'),
    ('Samarbete', 'Förmåga att arbeta väl i team'),
    ('Självständighet', 'Förmåga att agera på egen hand när det behövs'),
    ('Kreativitet', 'Förmåga att hitta innovativa lösningar'),
    ('Analytisk', 'Förmåga att analysera situationer noggrant'),
    ('Kommunikation', 'Förmåga att kommunicera effektivt')
]

# Sample scenario texts
SCENARIO_TEXTS = [
    "Du står inför ett kritiskt beslut där tiden är knapp. Hur agerar du?",
    "En kollega behöver din hjälp, men det kan äventyra ditt eget uppdrag. Vad gör du?",
    "Du upptäcker information som kan förändra hela situationen. Hur hanterar du detta?",
    "Teamet är oense om vägen framåt. Hur löser du konflikten?",
    "En oväntad händelse kräver omedelbar respons. Vilket val gör du?",
    "Du måste välja mellan att följa protokoll eller agera på egen hand. Vad väljer du?",
    "Resurser är begränsade och du måste prioritera. Hur fördelar du dem?",
    "En farlig situation kräver modiga beslut. Hur reagerar du?",
    "Du har möjlighet att hjälpa flera personer, men kan bara nå några. Vem väljer du?",
    "Information du fått visar sig vara felaktig. Hur justerar du din plan?"
]

# Sample choice option texts
CHOICE_OPTIONS = [
    {
        'option': 'Agera snabbt och beslutsamt',
        'outcome': 'Du tog ett modigt beslut som visade ledarskap.',
        'is_good': True
    },
    {
        'option': 'Vänta och samla mer information',
        'outcome': 'Din försiktighet visade sig vara klok.',
        'is_good': True
    },
    {
        'option': 'Konsultera teamet först',
        'outcome': 'Teamarbetet stärkte beslutet.',
        'is_good': True
    },
    {
        'option': 'Agera impulsivt utan att tänka',
        'outcome': 'Ditt snabba beslut ledde till oönskade konsekvenser.',
        'is_good': False
    },
    {
        'option': 'Ignorera situationen',
        'outcome': 'Din passivitet förvärrade situationen.',
        'is_good': False
    },
    {
        'option': 'Fokusera enbart på ditt eget mål',
        'outcome': 'Du nådde ditt mål men förlorade förtroende.',
        'is_good': False
    },
    {
        'option': 'Hjälpa alla så gott det går',
        'outcome': 'Din empati och vilja att hjälpa uppskattades.',
        'is_good': True
    },
    {
        'option': 'Följa protokoll strikt',
        'outcome': 'Protokollet visade sig vara rätt väg framåt.',
        'is_good': True
    }
]


def generate_users(db: Session, count: int = 200) -> List[User]:
    """Generate a specified number of users with random but realistic data"""
    print(f"Generating {count} users...")
    users = []
    
    for i in range(count):
        first_name = random.choice(FIRST_NAMES)
        username = f"{first_name.lower()}{random.randint(100, 999)}"
        age = random.randint(18, 65)
        
        user = User(
            username=username,
            gender=random.choice(GENDERS),
            age=age,
            occupation=random.choice(OCCUPATIONS),
            leadership_style=random.choice(LEADERSHIP_STYLES),
            priority=random.choice(PRIORITIES),
            team_role=random.choice(TEAM_ROLES),
            risk_tolerance=random.choice(RISK_TOLERANCES)
        )
        users.append(user)
    
    db.add_all(users)
    db.flush()
    print(f"Created {len(users)} users")
    return users


def generate_attributes(db: Session) -> List[Attribute]:
    """Generate all game attributes"""
    print("Generating attributes...")
    
    # Check if attributes already exist
    existing_attrs = db.query(Attribute).all()
    if existing_attrs:
        print(f"✓ Attributes already exist ({len(existing_attrs)} found)")
        return existing_attrs
    
    attributes = []
    for name, description in ATTRIBUTE_NAMES:
        attr = Attribute(name=name, description=description)
        attributes.append(attr)
    
    db.add_all(attributes)
    db.flush()
    print(f"Created {len(attributes)} attributes")
    return attributes


def generate_levels_and_scenarios(db: Session, num_levels: int = 5, scenarios_per_level: int = 4) -> tuple[List[Level], List[Scenario]]:
    """Generate levels and scenarios"""
    print(f"Generating {num_levels} levels with {scenarios_per_level} scenarios each...")
    
    levels = []
    scenarios = []
    
    for level_num in range(1, num_levels + 1):
        level = Level(
            level_number=level_num,
            title=f"Nivå {level_num}: Utmaning {level_num}"
        )
        levels.append(level)
        db.add(level)
        db.flush()
        
        # Create scenarios for this level
        for scenario_idx in range(scenarios_per_level):
            scenario_text = random.choice(SCENARIO_TEXTS)
            scenario = Scenario(
                level_id=level.level_id,
                scenario_text=f"{scenario_text} (Nivå {level_num}, Scenario {scenario_idx + 1})"
            )
            scenarios.append(scenario)
            db.add(scenario)
            db.flush()
    
    print(f"✓ Created {len(levels)} levels and {len(scenarios)} scenarios")
    return levels, scenarios


def generate_choice_options(db: Session, scenarios: List[Scenario]) -> List[ChoiceOption]:
    """Generate choice options for each scenario"""
    print(f"Generating choice options for {len(scenarios)} scenarios...")
    
    choice_options = []
    
    for scenario in scenarios:
        # Each scenario gets 3-4 choice options
        num_choices = random.randint(3, 4)
        selected_choices = random.sample(CHOICE_OPTIONS, min(num_choices, len(CHOICE_OPTIONS)))
        
        for choice_data in selected_choices:
            choice = ChoiceOption(
                scenario_id=scenario.scenario_id,
                option_text=choice_data['option'],
                outcome_text=choice_data['outcome'],
                is_good=choice_data['is_good']
            )
            choice_options.append(choice)
            db.add(choice)
            db.flush()
    
    print(f"✓ Created {len(choice_options)} choice options")
    return choice_options


def link_choice_attributes(db: Session, choice_options: List[ChoiceOption], attributes: List[Attribute]):
    """Link choice options to attributes with score changes"""
    print("Linking choice options to attributes...")
    
    links_created = 0
    for choice in choice_options:
        # Each choice affects 1-3 random attributes
        num_attributes = random.randint(1, 3)
        selected_attrs = random.sample(attributes, min(num_attributes, len(attributes)))
        
        for attr in selected_attrs:
            # Score change: -10 to +10, biased towards positive for good choices
            if choice.is_good:
                score_change = random.randint(1, 10)
            elif choice.is_good is False:
                score_change = random.randint(-10, -1)
            else:  # neutral
                score_change = random.randint(-5, 5)
            
            # Check if link already exists
            existing = db.execute(
                select(choice_attributes).where(
                    choice_attributes.c.choice_id == choice.choice_id,
                    choice_attributes.c.attribute_id == attr.attribute_id
                )
            ).first()
            
            if not existing:
                db.execute(
                    insert(choice_attributes).values(
                        choice_id=choice.choice_id,
                        attribute_id=attr.attribute_id,
                        score_change=score_change
                    )
                )
                links_created += 1
    
    db.flush()
    print(f"✓ Created {links_created} choice-attribute links")


def generate_user_choices(db: Session, users: List[User], scenarios: List[Scenario], 
                          choice_options: List[ChoiceOption], choices_per_user: int = 10):
    """Generate user choices - simulate users playing the game"""
    print(f"Generating user choices ({choices_per_user} per user)...")
    
    # Group choice options by scenario_id for quick lookup
    choices_by_scenario = {}
    for choice in choice_options:
        if choice.scenario_id not in choices_by_scenario:
            choices_by_scenario[choice.scenario_id] = []
        choices_by_scenario[choice.scenario_id].append(choice)
    
    # Group scenarios by level_id
    scenarios_by_level = {}
    for scenario in scenarios:
        if scenario.level_id not in scenarios_by_level:
            scenarios_by_level[scenario.level_id] = []
        scenarios_by_level[scenario.level_id].append(scenario)
    
    user_choices_list = []
    total_choices = 0
    
    for user in users:
        # Each user makes choices across different levels and scenarios
        selected_scenarios = random.sample(scenarios, min(choices_per_user, len(scenarios)))
        
        for scenario in selected_scenarios:
            # Pick a random choice option for this scenario
            available_choices = choices_by_scenario.get(scenario.scenario_id, [])
            if not available_choices:
                continue
            
            chosen_choice = random.choice(available_choices)
            
            user_choice = UserChoice(
                user_id=user.user_id,
                level_id=scenario.level_id,
                scenario_id=scenario.scenario_id,
                choice_id=chosen_choice.choice_id
            )
            user_choices_list.append(user_choice)
            total_choices += 1
    
    db.add_all(user_choices_list)
    db.flush()
    print(f"✓ Created {total_choices} user choices")
    
    return user_choices_list


def update_user_attributes_from_choices(db: Session, users: List[User], user_choices: List[UserChoice], 
                                        choice_options: List[ChoiceOption], attributes: List[Attribute]):
    """Update user attribute scores based on their choices"""
    print("Updating user attribute scores based on choices...")
    
    # Get all choice-attribute links
    choice_attr_links = {}
    result = db.execute(
        choice_attributes.select()
    )
    for row in result:
        choice_id = row.choice_id
        attr_id = row.attribute_id
        score_change = row.score_change
        if choice_id not in choice_attr_links:
            choice_attr_links[choice_id] = []
        choice_attr_links[choice_id].append((attr_id, score_change))
    
    # Group user choices by user_id
    choices_by_user = {}
    for uc in user_choices:
        if uc.user_id not in choices_by_user:
            choices_by_user[uc.user_id] = []
        choices_by_user[uc.user_id].append(uc)
    
    updates = 0
    for user in users:
        user_attr_scores = {}
        
        # Calculate scores for each attribute based on user's choices
        if user.user_id in choices_by_user:
            for user_choice in choices_by_user[user.user_id]:
                choice_id = user_choice.choice_id
                if choice_id in choice_attr_links:
                    for attr_id, score_change in choice_attr_links[choice_id]:
                        if attr_id not in user_attr_scores:
                            user_attr_scores[attr_id] = 0
                        user_attr_scores[attr_id] += score_change
        
        # Insert or update user_attributes
        for attr_id, score in user_attr_scores.items():
            # Ensure score is at least 0
            final_score = max(0, score)
            
            # Check if relationship already exists
            existing = db.execute(
                select(user_attributes.c.score).where(
                    user_attributes.c.user_id == user.user_id,
                    user_attributes.c.attribute_id == attr_id
                )
            ).first()
            
            if existing:
                # Update existing score
                db.execute(
                    update(user_attributes)
                    .where(
                        user_attributes.c.user_id == user.user_id,
                        user_attributes.c.attribute_id == attr_id
                    )
                    .values(score=final_score)
                )
            else:
                # Insert new relationship
                db.execute(
                    insert(user_attributes).values(
                        user_id=user.user_id,
                        attribute_id=attr_id,
                        score=final_score
                    )
                )
            updates += 1
    
    db.flush()
    print(f"✓ Updated {updates} user-attribute relationships")


def generate_all_data(num_users: int = 200, num_levels: int = 5, 
                     scenarios_per_level: int = 4, choices_per_user: int = 10,
                     clear_existing: bool = False):
    """
    Main function to generate all test data
    
    Args:
        num_users: Number of users to generate
        num_levels: Number of game levels
        scenarios_per_level: Number of scenarios per level
        choices_per_user: Number of choices each user makes
        clear_existing: If True, clears existing data first (WARNING: deletes all data!)
    """
    print("=" * 60)
    print("TEST DATA GENERATOR")
    print("=" * 60)
    
    db = SessionLocal()
    try:
        # Initialize database
        init_db()
        
        if clear_existing:
            print("\n⚠️  WARNING: Clearing existing data...")
            db.query(UserChoice).delete()
            db.query(ChoiceOption).delete()
            db.query(Scenario).delete()
            db.query(Level).delete()
            db.query(User).delete()
            db.query(Attribute).delete()
            db.commit()
            print("✓ Existing data cleared")
        
        # Generate data
        print("\n--- Generating Data ---")
        attributes = generate_attributes(db)
        users = generate_users(db, num_users)
        levels, scenarios = generate_levels_and_scenarios(db, num_levels, scenarios_per_level)
        choice_options = generate_choice_options(db, scenarios)
        
        print("\n--- Linking Data ---")
        link_choice_attributes(db, choice_options, attributes)
        user_choices = generate_user_choices(db, users, scenarios, choice_options, choices_per_user)
        update_user_attributes_from_choices(db, users, user_choices, choice_options, attributes)
        
        # Commit everything
        print("\n--- Committing to Database ---")
        db.commit()
        
        print("\n" + "=" * 60)
        print("✓ DATA GENERATION COMPLETE!")
        print("=" * 60)
        print(f"Users: {len(users)}")
        print(f"Attributes: {len(attributes)}")
        print(f"Levels: {len(levels)}")
        print(f"Scenarios: {len(scenarios)}")
        print(f"Choice Options: {len(choice_options)}")
        print(f"User Choices: {len(user_choices)}")
        print("=" * 60)
        
    except OperationalError as e:
        print(f"\n❌ FATAL ERROR: Database connection failed: {e}")
        print("Check that the database is running and DATABASE_URL is correct.")
        db.rollback()
        raise
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    # Generate data with default parameters
    # Set clear_existing=True to clear all existing data first (use with caution!)
    generate_all_data(
        num_users=200,
        num_levels=5,
        scenarios_per_level=4,
        choices_per_user=10,
        clear_existing=False  # Set to True to clear existing data
    )
