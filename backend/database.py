from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
import config
from typing import Annotated
from fastapi import Depends
import os


DATABASE_URL = config.database_url

if not os.path.exists(config.data_directory):
    os.makedirs(config.data_directory)
    
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
