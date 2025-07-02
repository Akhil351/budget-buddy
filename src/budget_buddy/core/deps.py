from typing import Annotated
from sqlalchemy.orm import Session
from src.budget_buddy.database import SessionLocal

# DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


