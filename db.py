import psycopg2
from psycopg2 import sql
import pandas as pd
from config import DATABASE_URL

def get_connection():
    """Anslut till databasen"""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except psycopg2.Error as e:
        print(f"Fel vid databasanslutning: {e}")
        return None

def get_statistics():
    """Hämta all statistik från databasen"""
    conn = get_connection()
    if not conn:
        return None
    
    try:
        query = """
        SELECT user_id, question, answer, response_count 
        FROM user_responses 
        ORDER BY created_at DESC
        """
        df = pd.read_sql(query, conn)
        return df
    except Exception as e:
        print(f"Fel vid SQL-fråga: {e}")
        return None
    finally:
        if conn:
            conn.close()

def get_accounts(limit: int = 100):
    """Hämta lista över konton/användare från databasen.
    Försöker hitta en lämplig tabell (personer, users, accounts) och returnerar en DataFrame.
    """
    conn = get_connection()
    if not conn:
        return None

    try:
        # Hämta alla tabeller i public schema
        cursor = conn.cursor()
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
        tables = [r[0] for r in cursor.fetchall()]

        # Prioritera vanliga tabellnamn
        candidates = ['personer', 'users', 'accounts', 'persons', 'user_accounts']
        table_to_use = None
        for c in candidates:
            if c in tables:
                table_to_use = c
                break

        # Om ingen kandidat hittades, försök hitta en tabell med 'user' eller 'person' i namnet
        if not table_to_use:
            for t in tables:
                if 'user' in t.lower() or 'person' in t.lower():
                    table_to_use = t
                    break

        if not table_to_use:
            return None

        query = sql.SQL("SELECT * FROM {} LIMIT %s").format(sql.Identifier(table_to_use))
        df = pd.read_sql(query.as_string(conn), conn, params=(limit,))
        return df
    except Exception as e:
        print(f"Fel vid hämtning av konton: {e}")
        return None
    finally:
        try:
            cursor.close()
        except Exception:
            pass
        if conn:
            conn.close()

def get_question_statistics(question_text):
    """Hämta statistik för en specifik fråga"""
    conn = get_connection()
    if not conn:
        return None
    
    try:
        query = """
        SELECT answer, COUNT(*) as count 
        FROM user_responses 
        WHERE question = %s 
        GROUP BY answer
        ORDER BY count DESC
        """
        df = pd.read_sql(query, conn, params=(question_text,))
        return df
    except Exception as e:
        print(f"Fel vid SQL-fråga: {e}")
        return None
    finally:
        if conn:
            conn.close()

def save_user_response(user_id, question, answer):
    """Spara användarens svar till databasen"""
    conn = get_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        insert_query = """
        INSERT INTO user_responses (user_id, question, answer, created_at)
        VALUES (%s, %s, %s, NOW())
        """
        cursor.execute(insert_query, (user_id, question, answer))
        conn.commit()
        return True
    except Exception as e:
        print(f"Fel vid insertering: {e}")
        conn.rollback()
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
