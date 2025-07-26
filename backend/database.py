from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
import config
from typing import Annotated
from fastapi import Depends

DATABASE_URL = config.database_url

print(f"Connecting to database at {DATABASE_URL}")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

DbSession = Annotated[Session, Depends(get_db)]
