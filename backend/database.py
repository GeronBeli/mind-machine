from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from fastapi import Depends
from typing import Annotated


DATABASE_URL = "sqlite:///./userid_search_history_admin.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

def get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()


db_dependency = Annotated[Session, Depends(get_db)]