from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import OperationalError

#fixa .env fil för att inte lägga in lösenord och användarnamn i koden så vi ej pushar det till github
#fixa även logiken med database_url
DATABASE_URL = "postgresql://postgres:flatron7553@localhost:5432/test_db"

try:
    engine = create_engine(DATABASE_URL, echo=True)  # echo=True loggar alla sql frågor till konsolen
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
    """
    Base.metadata.create_all(bind=engine)
