from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

#fixa .env fil för att inte lägga in lösenord och användarnamn i koden så vi ej pushar det till github
#fixa även logiken med database_url
DATABASE_URL = "postgresql://användarnamn:lösenord@localhost:5432/databasnamn"


engine = create_engine(DATABASE_URL, echo=True)#echo=True loggar alla sql frågor till konsolen

"""
skapar session-fabrik för databassessioner
autocommit=False: ändringar kräver explicit commit
autoflush=False: Flush-operationer måste anropas explicit
"""
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

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
