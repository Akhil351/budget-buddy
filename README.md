# 🧠 Personal Finance Assistant (CLI Agent)

A simple yet powerful CLI-based personal finance assistant powered by OpenAI's function-calling capabilities and Bun runtime. It helps users:

- 🧾 Track **expenses**
- 💰 Record **income**
- 📊 View **current balance**
- 📆 Get total expenses for a specific date range

---

## 🚀 Setup & Run

### 1. Install dependencies
```bash
bun install
```

### 2. Run the app
```bash
bun run index.js
```

💡 **Make sure to set your OpenAI API key in your environment:**
```bash
export OPENAI_API_KEY=your_key_here
```

---

## 🛠 Features

| Feature           | Description                                         |
|-------------------|-----------------------------------------------------|
| addExpense        | Adds a new expense with name and amount             |
| addIncome         | Adds a new income record                            |
| getMoneyBalance   | Calculates and shows current balance (income - expenses) |
| getTotalExpense   | Fetches total expenses between two given dates      |

---

## 🧱 Built With

- 🦊 **Bun**: All-in-one JavaScript runtime (super fast)
- 🧠 **OpenAI**: Function-calling with gpt-4o
- 💻 **Node.js readline**: For terminal interaction

---

## 📁 Project Structure

```
index.js         # Main CLI agent code
.env             # Add your OpenAI API key here (optional)
README.md        # You're here!
```

---

## 📝 Example Interaction

```bash
User: I bought groceries for 1200 INR
Assistant: Expense recorded: "Bought groceries for 1200 INR" - ₹1200

User: Add income of 20000 INR from salary
Assistant: Income recorded: "salary" - ₹20000

User: What's my balance?
Assistant: Current balance: ₹18800

User: Total expenses from 2024-06-01 to 2024-06-20?
Assistant: Total expenses from 2024-06-01 to 2024-06-20: ₹1200
```

---

## ✅ Requirements

- Bun v1.2.17+ installed
- OpenAI API key with access to gpt-4o, gpt-4, or gpt-3.5-turbo

---

## 🙌 Credits

Built with 💻 by Akhil (your finance tech ninja 😎)

---

Let me know if you also want a `.env.example` template file to go with this.
