import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker 

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set.")
print("Connected to DB:", DATABASE_URL)
    
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# run_test_connection.py
from app.db.session import engine

try:
    with engine.connect() as conn:
        print("✅ PostgreSQL connected successfully!")
except Exception as e:
    print("❌ Error connecting to PostgreSQL:", e)
