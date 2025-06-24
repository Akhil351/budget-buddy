import OpenAI from "openai";
import readline from "node:readline/promises";

// In-memory databases
const expenseDB = [];
const incomeDB = [];

// Initialize OpenAI client
const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

// Main function to start the finance assistant
const startAssistant = async () => {
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
  });

  const messages = [
    {
      role: "system",
      content:
        "You are Akhil, a personal finance assistant. Your job is to help users manage expenses, record income, check balances, and assist with financial planning.",
    },
  ];

  while (true) {
    const userInput = await rl.question("User: ");
    if (userInput.toLowerCase() === "bye") break;

    messages.push({ role: "user", content: userInput });

    while (true) {
      const completion = await openai.chat.completions.create({
        messages,
        model: "gpt-4o",
        tools: [
          {
            type: "function",
            function: {
              name: "getTotalExpense",
              description:
                "Returns the total amount spent by the user during a specific date range. Useful for analyzing spending habits.",
              parameters: {
                type: "object",
                properties: {
                  from: {
                    type: "string",
                    description: "Start date (YYYY-MM-DD)",
                  },
                  to: {
                    type: "string",
                    description: "End date (YYYY-MM-DD)",
                  },
                },
                required: ["from", "to"],
              },
            },
          },
          {
            type: "function",
            function: {
              name: "getMoneyBalance",
              description:
                "Calculates and returns the remaining balance by subtracting total expenses from total income.",
            },
          },
          {
            type: "function",
            function: {
              name: "addIncome",
              description: "Adds a new income record to the income database.",
              parameters: {
                type: "object",
                properties: {
                  name: {
                    type: "string",
                    description:
                      "Description of the income (e.g., 'Salary for June')",
                  },
                  amount: {
                    type: "string",
                    description: "Amount of income received (in INR)",
                  },
                },
                required: ["name", "amount"],
              },
            },
          },
          {
            type: "function",
            function: {
              name: "addExpense",
              description: "Adds a new expense record to the expense database.",
              parameters: {
                type: "object",
                properties: {
                  name: {
                    type: "string",
                    description:
                      "Description of the expense (e.g., 'Bought groceries for 1200 INR')",
                  },
                  amount: {
                    type: "string",
                    description: "Amount spent (in INR)",
                  },
                },
                required: ["name", "amount"],
              },
            },
          },
        ],
      });

      const aiMessage = completion.choices[0].message;
      messages.push(aiMessage);

      const toolCalls = aiMessage.tool_calls;
      if (!toolCalls) {
        console.log(`Assistant: ${aiMessage.content}`);
        break;
      }

      for (const toolCall of toolCalls) {
        const functionName = toolCall.function.name;
        const args = JSON.parse(toolCall.function.arguments);
        let result = "";

        if (functionName === "getTotalExpense") {
          result = getTotalExpense(args);
        } else if (functionName === "addExpense") {
          result = addExpense(args);
        } else if (functionName === "addIncome") {
          result = addIncome(args);
        } else if (functionName === "getMoneyBalance") {
          result = getMoneyBalance();
        }

        messages.push({
          role: "tool",
          content: result,
          tool_call_id: toolCall.id,
        });
      }
    }
  }

  rl.close();
};

// Helper functions
const addExpense = ({ name, amount }) => {
  expenseDB.push({ name, amount: parseFloat(amount) });
  return `Expense recorded: "${name}" - ₹${amount}`;
};

const addIncome = ({ name, amount }) => {
  incomeDB.push({ name, amount: parseFloat(amount) });
  return `Income recorded: "${name}" - ₹${amount}`;
};

const getTotalExpense = ({ from, to }) => {
  const total = expenseDB.reduce((sum, entry) => sum + entry.amount, 0);
  return `Total expenses from ${from} to ${to}: ₹${total}`;
};

const getMoneyBalance = () => {
  const totalIncome = incomeDB.reduce((sum, entry) => sum + entry.amount, 0);
  const totalExpense = expenseDB.reduce((sum, entry) => sum + entry.amount, 0);
  return `Current balance: ₹${totalIncome - totalExpense}`;
};

// Start the assistant
startAssistant();
