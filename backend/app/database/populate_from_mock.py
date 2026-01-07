"""
Populate Database from mock.json
=================================
Läser scenarier från mock.json och skapar levels, scenarios, choice_options och attributes i databasen.
"""

import sys
import os
import json
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError

from backend.app.database.database import SessionLocal, init_db
from backend.app.database.models import (
    Level, Scenario, ChoiceOption, Attribute
)
from backend.app.database.crud import link_choice_to_attribute

# Attribut som används i spelet
ATTRIBUTES = [
    ("taktisk", "Tänker strategiskt och planerar framåt."),
    ("logisk", "Analyserar situationer rationellt."),
    ("lojal", "Sätter gruppen före sig själv."),
    ("omtänksam", "Bryr sig om andra i svåra situationer."),
    ("riskbenägen", "Tar modiga men riskfyllda val."),
    ("försiktig", "Undviker risk och spelar säkert."),
    ("pragmatisk", "Väljer det som fungerar bäst i praktiken."),
    ("moralisk", "Prioriterar etik över effektivitet."),
]


def load_mock_scenarios():
    """Läser scenarier från mock.json"""
    mock_file = project_root / "mock_data" / "mock.json"
    with open(mock_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data["scenarios"]


def create_attributes(db: Session):
    """Skapar attribut i databasen om de inte redan finns"""
    print("Creating attributes...")
    attributes_dict = {}
    
    for name, description in ATTRIBUTES:
        # Kolla om attributet redan finns
        existing = db.query(Attribute).filter(Attribute.name == name).first()
        if existing:
            attributes_dict[name] = existing
            print(f"  Attribute '{name}' already exists")
        else:
            attr = Attribute(name=name, description=description)
            db.add(attr)
            db.flush()
            attributes_dict[name] = attr
            print(f"  Created attribute: {name}")
    
    db.commit()
    return attributes_dict


def create_levels_and_scenarios(db: Session, scenarios_data):
    """Skapar levels och scenarios från mock.json data"""
    print("Creating levels and scenarios...")
    
    # Skapa en level för alla scenarier (eller flera levels om du vill)
    level = Level(
        level_number=1,
        title="Krisens första dag"
    )
    db.add(level)
    db.flush()
    print(f"  Created level: {level.title}")
    
    scenarios_list = []
    for idx, scenario_data in enumerate(scenarios_data, 1):
        scenario = Scenario(
            level_id=level.level_id,
            scenario_text=scenario_data["text"]
        )
        db.add(scenario)
        db.flush()
        scenarios_list.append((scenario, scenario_data))
        print(f"  Created scenario {idx}: {scenario_data.get('title', f'Scenario {idx}')[:50]}...")
    
    db.commit()
    return scenarios_list


def create_choice_options(db: Session, scenarios_list):
    """Skapar choice_options från mock.json data"""
    print("Creating choice options...")
    
    choice_options_list = []
    for scenario, scenario_data in scenarios_list:
        # Skapa val A
        choice_a = ChoiceOption(
            scenario_id=scenario.scenario_id,
            option_text=scenario_data["a"],
            outcome_text=scenario_data.get("right_msg", "") if scenario_data["correct"] == "a" else scenario_data.get("wrong_msg", ""),
            is_good=(scenario_data["correct"] == "a")
        )
        db.add(choice_a)
        db.flush()
        choice_options_list.append((choice_a, scenario_data, "a"))
        
        # Skapa val B
        choice_b = ChoiceOption(
            scenario_id=scenario.scenario_id,
            option_text=scenario_data["b"],
            outcome_text=scenario_data.get("right_msg", "") if scenario_data["correct"] == "b" else scenario_data.get("wrong_msg", ""),
            is_good=(scenario_data["correct"] == "b")
        )
        db.add(choice_b)
        db.flush()
        choice_options_list.append((choice_b, scenario_data, "b"))
        
        print(f"  Created 2 choices for scenario {scenario.scenario_id}")
    
    db.commit()
    return choice_options_list


def link_attributes_to_choices(db: Session, choice_options_list, attributes_dict):
    """Länkar attribut till val baserat på valets karaktär"""
    print("Linking attributes to choices...")
    
    links_created = 0
    
    for choice_option, scenario_data, choice_letter in choice_options_list:
        is_correct = choice_option.is_good
        
        # Baserat på valets text och om det är korrekt/felaktigt, länka till relevanta attribut
        choice_text = choice_option.option_text.lower()
        
        # Logik för att länka attribut baserat på valets innehåll
        if is_correct:
            # Korrekta val ökar positiva attribut
            if "stannar" in choice_text or "följer" in choice_text or "officiella" in choice_text:
                # Taktisk, logisk, försiktig
                for attr_name in ["taktisk", "logisk", "försiktig"]:
                    if attr_name in attributes_dict:
                        link_choice_to_attribute(db, choice_option.choice_id, attributes_dict[attr_name].attribute_id, 5)
                        links_created += 1
            
            if "hjälper" in choice_text or "solidaritet" in choice_text or "ansvar" in choice_text:
                # Lojal, omtänksam, moralisk
                for attr_name in ["lojal", "omtänksam", "moralisk"]:
                    if attr_name in attributes_dict:
                        link_choice_to_attribute(db, choice_option.choice_id, attributes_dict[attr_name].attribute_id, 5)
                        links_created += 1
        else:
            # Felaktiga val ökar negativa eller minskar positiva attribut
            if "cyklar hem" in choice_text or "impulsiv" in choice_text:
                # Riskbenägen, minskar försiktig
                if "riskbenägen" in attributes_dict:
                    link_choice_to_attribute(db, choice_option.choice_id, attributes_dict["riskbenägen"].attribute_id, 3)
                    links_created += 1
                if "försiktig" in attributes_dict:
                    link_choice_to_attribute(db, choice_option.choice_id, attributes_dict["försiktig"].attribute_id, -3)
                    links_created += 1
            
            if "stannar i kön" in choice_text or "egen" in choice_text:
                # Minskar lojalitet, omtänksamhet
                for attr_name in ["lojal", "omtänksam"]:
                    if attr_name in attributes_dict:
                        link_choice_to_attribute(db, choice_option.choice_id, attributes_dict[attr_name].attribute_id, -3)
                        links_created += 1
    
    db.commit()
    print(f"  Created {links_created} attribute links")


def populate_database(db: Session = None):
    """Huvudfunktion som populerar databasen från mock.json
    
    Args:
        db: Optional database session. If None, creates a new one.
    """
    print("=" * 60)
    print("POPULATING DATABASE FROM mock.json")
    print("=" * 60)
    
    # Läs mock.json
    scenarios_data = load_mock_scenarios()
    print(f"\nLoaded {len(scenarios_data)} scenarios from mock.json\n")
    
    if db is None:
        db = SessionLocal()
        should_close = True
    else:
        should_close = False
    
    try:
        # Skapa attribut
        attributes_dict = create_attributes(db)
        
        # Skapa levels och scenarios
        scenarios_list = create_levels_and_scenarios(db, scenarios_data)
        
        # Skapa choice_options
        choice_options_list = create_choice_options(db, scenarios_list)
        
        # Länka attribut till val
        link_attributes_to_choices(db, choice_options_list, attributes_dict)
        
        print("\n" + "=" * 60)
        print("DATABASE POPULATION COMPLETE!")
        print("=" * 60)
        print(f"Attributes: {len(attributes_dict)}")
        print(f"Scenarios: {len(scenarios_list)}")
        print(f"Choice options: {len(choice_options_list)}")
        print("=" * 60)
        
    except OperationalError as e:
        print(f"\nFATAL ERROR: Database connection failed: {e}")
        print("Check that the database is running and DATABASE_URL is correct.")
        db.rollback()
        raise
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        if db:
            db.rollback()
        raise
    finally:
        if should_close and db:
            db.close()


if __name__ == "__main__":
    populate_database()
