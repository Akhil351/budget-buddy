# 📁 service/finance_tools.py

from langchain_core.tools import tool
import datetime
from sqlalchemy.orm import Session
from src.budget_buddy.core.deps import get_db
from src.budget_buddy.models import Transaction, TransactionType
from sqlalchemy import func

# Helper function to format amount as ₹XX,XXX.00
def format_inr(amount: float) -> str:
    return f"₹{amount:,.2f}"

@tool
def add_income(name: str, amount: float) -> str:
    """Add an income entry."""
    db = next(get_db())
    try:
        transaction = Transaction(
            name=name,
            amount=amount,
            type=TransactionType.INCOME,
            date=datetime.date.today().isoformat()
        )
        db.add(transaction)
        db.commit()
        return f"✅ Income of {format_inr(amount)} added: {name}"
    except Exception as e:
        db.rollback()
        return f"❌ Error adding income: {str(e)}"

@tool
def add_expense(name: str, amount: float) -> str:
    """Add an expense entry."""
    db = next(get_db())
    try:
        transaction = Transaction(
            name=name,
            amount=amount,
            type=TransactionType.EXPENSE,
            date=datetime.date.today().isoformat()
        )
        db.add(transaction)
        db.commit()
        return f"💸 Expense of {format_inr(amount)} added: {name}"
    except Exception as e:
        db.rollback()
        return f"❌ Error adding expense: {str(e)}"

@tool
def get_balance() -> str:
    """Get net balance from income and expense."""
    db = next(get_db())
    try:
        # Get total income
        total_income = db.query(Transaction).filter(
            Transaction.type == TransactionType.INCOME
        ).with_entities(func.sum(Transaction.amount)).scalar() or 0.0
        
        # Get total expense
        total_expense = db.query(Transaction).filter(
            Transaction.type == TransactionType.EXPENSE
        ).with_entities(func.sum(Transaction.amount)).scalar() or 0.0
        
        net_balance = total_income - total_expense
        return f"📊 Current balance is {format_inr(net_balance)}"
    except Exception as e:
        return f"❌ Error getting balance: {str(e)}"

@tool
def get_total_income(from_date: str, to_date: str) -> str:
    """Get total income in date range (format: YYYY-MM-DD)."""
    db = next(get_db())
    try:
        total = db.query(Transaction).filter(
            Transaction.type == TransactionType.INCOME,
            Transaction.date >= from_date,
            Transaction.date <= to_date
        ).with_entities(func.sum(Transaction.amount)).scalar() or 0.0
        
        return f"💰 Income from {from_date} to {to_date}: {format_inr(total)}"
    except Exception as e:
        return f"❌ Error getting total income: {str(e)}"

@tool
def get_total_expense(from_date: str, to_date: str) -> str:
    """Get total expense in date range (format: YYYY-MM-DD)."""
    db = next(get_db())
    try:
        total = db.query(Transaction).filter(
            Transaction.type == TransactionType.EXPENSE,
            Transaction.date >= from_date,
            Transaction.date <= to_date
        ).with_entities(func.sum(Transaction.amount)).scalar() or 0.0
        
        return f"💸 Expense from {from_date} to {to_date}: {format_inr(total)}"
    except Exception as e:
        return f"❌ Error getting total expense: {str(e)}"

@tool
def get_today_date() -> str:
    """Return today's date in YYYY-MM-DD format."""
    return f"📅 Today's date is {datetime.date.today()}"

# Export tool list for convenience
TOOLS = [
    add_income,
    add_expense,
    get_balance,
    get_total_income,
    get_total_expense,
    get_today_date,
] 