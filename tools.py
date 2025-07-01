### 📁 File: tools.py

from langchain_core.tools import tool
import datetime

# In-memory databases (you can later replace these with PostgreSQL or any DB)
income_db = []
expense_db = []

# Helper function to format amount as ₹XX,XXX.00
def format_inr(amount: float) -> str:
    return f"₹{amount:,.2f}"

@tool
def add_income(name: str, amount: float) -> str:
    """Add an income entry."""
    income_db.append({
        "name": name,
        "amount": amount,
        "date": str(datetime.date.today())
    })
    return f"✅ Income of {format_inr(amount)} added: {name}"

@tool
def add_expense(name: str, amount: float) -> str:
    """Add an expense entry."""
    expense_db.append({
        "name": name,
        "amount": amount,
        "date": str(datetime.date.today())
    })
    return f"💸 Expense of {format_inr(amount)} added: {name}"

@tool
def get_balance() -> str:
    """Get net balance from income and expense."""
    total_income = sum(x["amount"] for x in income_db)
    total_expense = sum(x["amount"] for x in expense_db)
    net_balance = total_income - total_expense
    return f"📊 Current balance is {format_inr(net_balance)}"

@tool
def get_total_income(from_date: str, to_date: str) -> str:
    """Get total income in date range (format: YYYY-MM-DD)."""
    from_dt = datetime.date.fromisoformat(from_date)
    to_dt = datetime.date.fromisoformat(to_date)
    total = sum(
        x["amount"]
        for x in income_db
        if from_dt <= datetime.date.fromisoformat(x["date"]) <= to_dt
    )
    return f"💰 Income from {from_date} to {to_date}: {format_inr(total)}"

@tool
def get_total_expense(from_date: str, to_date: str) -> str:
    """Get total expense in date range (format: YYYY-MM-DD)."""
    from_dt = datetime.date.fromisoformat(from_date)
    to_dt = datetime.date.fromisoformat(to_date)
    total = sum(
        x["amount"]
        for x in expense_db
        if from_dt <= datetime.date.fromisoformat(x["date"]) <= to_dt
    )
    return f"💸 Expense from {from_date} to {to_date}: {format_inr(total)}"

@tool
def get_today_date() -> str:
    """Return today's date in YYYY-MM-DD format."""
    return f"📅 Today's date is {datetime.date.today()}"

# Export tool list
TOOLS = [
    add_income,
    add_expense,
    get_balance,
    get_total_income,
    get_total_expense,
    get_today_date,
]
