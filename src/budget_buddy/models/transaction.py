from sqlalchemy import Column, Integer, String, Float, DateTime, Enum
from sqlalchemy.sql import func
from enum import Enum as PythonEnum
from src.budget_buddy.database import Base

class TransactionType(PythonEnum):
    """Transaction type enum."""
    INCOME = "income"
    EXPENSE = "expense"

class Transaction(Base):
    """Transaction model for storing both income and expense entries."""
    
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    amount = Column(Float, nullable=False)
    type = Column(Enum(TransactionType), nullable=False, index=True)
    date = Column(String(10), nullable=False, index=True)  # YYYY-MM-DD format
    created_at = Column(DateTime, default=func.now())