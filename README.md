# Finance Assistant

A command-line AI-powered finance assistant to help you track your income, expenses, and balances. Built with [LangGraph](https://github.com/langchain-ai/langgraph), [LangChain](https://github.com/langchain-ai/langchain), and OpenAI's GPT-4o.

---

## Features

- **Add Income**: Log new income entries with name and amount.
- **Add Expense**: Log new expense entries with name and amount.
- **Get Balance**: View your current net balance.
- **Get Total Income/Expense**: Query total income or expenses for a date range.
- **Get Today's Date**: Ask for the current date.
- **Conversational AI**: Interact naturally with the assistant in a chat-like CLI.

---

## Quickstart

### 1. Requirements
- Python **3.13** (see `.python-version`)
- [OpenAI API Key](https://platform.openai.com/account/api-keys)

### 2. Installation

Clone the repo and install dependencies:

```bash
# Clone this repository
$ git clone <your-repo-url>
$ cd Finance_Assitant

# (Recommended) Create a virtual environment
$ python3.13 -m venv .venv
$ source .venv/bin/activate

# Install dependencies
$ pip install -r requirements.txt  # or use a tool like uv/poetry
```

> **Note:** Dependencies are also listed in `pyproject.toml` and locked in `uv.lock`.

### 3. Environment Setup

Create a `.env` file in the project root with your OpenAI API key:

```
OPENAI_API_KEY=sk-...
```

### 4. Run the Assistant

```bash
$ python main.py
```

You should see:
```
🤖 Finance Assistant Ready! (Type 'exit' to quit)
You: 
```
Type your queries (e.g., "Add income Salary 50000", "What is my balance?", "Add expense Groceries 1200", etc.).

---

## How It Works

- **main.py**: Runs a CLI chat loop, sending user messages to the agent and printing responses.
- **agent.py**: Sets up the LangGraph agent, binds OpenAI GPT-4o with finance tools, and manages the conversation flow.
- **tools.py**: Implements the finance tools (add income/expense, get balance, etc.) using in-memory lists.
- **.env**: Stores your OpenAI API key (not committed to git).

---

## Tool Functions

- `add_income(name: str, amount: float)` — Add an income entry.
- `add_expense(name: str, amount: float)` — Add an expense entry.
- `get_balance()` — Get net balance from income and expense.
- `get_total_income(from_date: str, to_date: str)` — Get total income in a date range (YYYY-MM-DD).
- `get_total_expense(from_date: str, to_date: str)` — Get total expense in a date range (YYYY-MM-DD).
- `get_today_date()` — Get today's date in YYYY-MM-DD format.

---

## Development Notes

- **Data Storage**: All data is stored in-memory (lists). Data will be lost when the program exits. For persistence, connect to a database (see `tools.py`).
- **Dependencies**: See `pyproject.toml` for main dependencies. Use `uv.lock` for reproducible installs.
- **.gitignore**: Ignores Python cache, build files, virtual environments, and `.env`/`.txt` files.
- **Python Version**: Uses Python 3.13 (see `.python-version`).

---

## License

MIT (or specify your license here)

---

## Credits

- [LangChain](https://github.com/langchain-ai/langchain)
- [LangGraph](https://github.com/langchain-ai/langgraph)
- [OpenAI](https://platform.openai.com/)
