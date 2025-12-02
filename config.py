import os
from dotenv import load_dotenv

# Ladda .env filen
load_dotenv()

# Databaskonfiguration
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL är inte inställd i .env filen")
