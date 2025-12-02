from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import OperationalError

#fixa .env fil för att inte lägga in lösenord och användarnamn i koden så vi ej pushar det till github
#fixa även logiken med database_url
DATABASE_URL = "postgresql://postgres:allansikder2005@localhost:5432/msbhack_test"

try:
    engine = create_engine(DATABASE_URL, echo=False)  # echo=True loggar alla sql frågor till konsolen
    # Testa anslutningen
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    print("Database connection successful!")
except OperationalError as e:
    print(f"Database connection failed: {e}")
    raise
except Exception as e:
    print(f"Database connection error: {e}")
    raise

"""
skapar session-fabrik för databassessioner
autocommit=False: ändringar kräver explicit commit
autoflush=False: Flush-operationer måste anropas explicit
"""
if engine:
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
else:
    SessionLocal = None

"""basklass för deklarativa modeller
   alla databasmodeller bör ärva från denna Base"""
Base = declarative_base()




def get_db():
    """
    Generatorfunktion för att få en databassession.
    Returnerar en databassession och säkerställer att den stängs efter användning.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Skapar alla tabeller i databasen.
    Används för att initialisera databasen första gången.
    Om tabellerna redan finns, migrerar den dem till nytt schema.
    """
    # Droppa alla tabeller först (varning: förlorar data!)
    # Base.metadata.drop_all(bind=engine)
    
    # Skapa alla tabeller med nytt schema
    Base.metadata.create_all(bind=engine)
    
    # Migrera users-tabellen - lägg till nya kolumner om de saknas
    try:
        with engine.connect() as conn:
            # Kolla vilka kolumner som finns
            result = conn.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'users'
            """))
            existing_columns = {row[0] for row in result}
            
            # Lista över kolumner som ska finnas enligt modellen
            required_columns = {
                'username', 'gender', 'age', 'occupation', 
                'leadership_style', 'priority', 'team_role', 'risk_tolerance'
            }
            
            missing_columns = required_columns - existing_columns
            
            if missing_columns:
                print(f"Migrating users table - adding columns: {missing_columns}")
                # Lägg till saknade kolumner
                if 'username' in missing_columns:
                    conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS username VARCHAR(50)"))
                if 'gender' in missing_columns:
                    conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS gender VARCHAR(50)"))
                if 'occupation' in missing_columns:
                    conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS occupation VARCHAR(50)"))
                if 'leadership_style' in missing_columns:
                    conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS leadership_style VARCHAR(50)"))
                if 'priority' in missing_columns:
                    conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS priority VARCHAR(50)"))
                if 'team_role' in missing_columns:
                    conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS team_role VARCHAR(50)"))
                if 'risk_tolerance' in missing_columns:
                    conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS risk_tolerance VARCHAR(50)"))
                conn.commit()
                print("Migration complete!")
    except Exception as e:
        print(f"Migration note: {e}")
        # Fortsätt ändå - tabellerna kanske redan är korrekta
