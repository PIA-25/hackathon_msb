from __future__ import annotations
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError

# OBS! Dessa imports MÅSTE vara korrekta i din struktur
from backend.app.database.database import SessionLocal, init_db
from backend.app.database.models import User, Attribute, Level, Scenario, ChoiceOption # Importera alla modeller

def insert_initial_data(db: Session):
    """
    Sätter in grundläggande testdata i databasen.
    """
    print("--- Startar databasinitiering och insättning av testdata ---")
    
    # Kör init_db för att säkerställa att tabellerna finns
    init_db()

    # Kontrollera om data redan finns (Hämtning)
    if db.query(User).count() > 0:
        print("Databasen är redan fylld med testdata. Hoppar över insättning.")
        return
    
    attributes_user = [
        {"name": "taktisk", "description": "Tänker strategiskt och planerar framåt."},
        {"name": "logisk", "description": "Analyserar situationer rationellt."},
        {"name": "lojal", "description": "Sätter gruppen före sig själv."},
        {"name": "omtänksam", "description": "Bryr sig om andra i svåra situationer."},
        {"name": "riskbenägen", "description": "Tar modiga men riskfyllda val."},
        {"name": "försiktig", "description": "Undviker risk och spelar säkert."},
        {"name": "pragmatisk", "description": "Väljer det som fungerar bäst i praktiken."},
        {"name": "moralisk", "description": "Prioriterar etik över effektivitet."}
    ]
    # Loopar igenom listan och skapar Attribute-objekt
    for attr in attributes_user:
        db.add(Attribute(name=attr["name"], description=attr["description"]))
        
    # --- 2. SKAPA ANVÄNDARE ---
    user_alice = User(firstname="Alice", lastname="Test", age=25, krigsberedd=True)
    user_bob = User(firstname="Bob", lastname="Test", age=35, krigsberedd=False)
    
    db.add_all([user_alice, user_bob])

    db.commit()
    print("✓ Insättning lyckades: 2 användare och 2 attribut har lagts till.")


def test_fetch_data():
    """Hämtar och skriver ut alla användare och attribut."""
    
    db: Session = SessionLocal()
    try:
        print("\n--- TEST: Hämta data från 'users' och 'attributes' ---")
        
        # Hämta alla användare
        users = db.query(User).all()
        
        if users:
            print(f"✓ Hämntning lyckades! Hittade {len(users)} användare:")
            for user in users:
                print(f"  ID: {user.user_id}, Namn: {user.firstname} {user.lastname}, Ålder: {user.age}")
        else:
            print("✗ Tabellen 'users' är tom.")
            
        # Hämta alla attribut
        attributes = db.query(Attribute).all()
        if attributes:
            print(f"✓ Hittade {len(attributes)} attribut.")
            for attr in attributes:
                print(f" ID: {attr.attribute_id}, Namn: {attr.name}, Beskrivning: {attr.description}")
            else:
                print("✗ Tabellen 'attributes' är tom")

    except Exception as e:
        print(f"✗ Fel vid datahämtning: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    # Öppnar en session för att köra testerna
    try:
        # FÖRSTA GÅNGEN: Sätter in testdata (inklusive tabellskapande)
        db = SessionLocal()
        insert_initial_data(db)
    except OperationalError as oe:
        print(f"\n✗ FATALT FEL: Databasanslutningen misslyckades vid insättning: {oe}")
        print("Kontrollera att databasen 'testhackaton' körs och att lösenordet i DATABASE_URL är korrekt.")
    
    # KÖR HÄMTNINGSTESTET
    test_fetch_data()
