from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError, OperationalError

DATABASE_URL = "postgresql://postgres:namn@localhost:5432/dbnamn"

engine = create_engine(
    DATABASE_URL,
    echo=True )

def create_connection():
    """Skapar och returnerar en anslutning till PostgreSQL-databasen."""
    try:
        connection = engine.connect()
        print("Anslutning till PostgreSQL lyckades")
        return connection
    except OperationalError as e:
        print(f"FEL: Kunde inte ansluta till databasen. Kontrollera att PostgreSQL körs och att URL är korrekt.")
        print(f"Detaljerat fel: {e}")
        return None
    except SQLAlchemyError as e:
        print(f"Ett SQLAlchemy-fel inträffade: '{e}'")
        return None

def close_connection(connection):
    """Stänger databasanslutningen."""
    if connection:
        connection.close()
        print("Anslutning stängd.")


#testkod som körs när filen körs direkt
if __name__ == '__main__':
    print("Testar anslutningen...")
    connection = create_connection()
    if connection:
        print("Anslutningstest lyckades.")
        close_connection(connection)
    else:
        print("Anslutningstest misslyckades.")