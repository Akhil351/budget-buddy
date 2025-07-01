# 📁 main.py

from agent import app
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
import json
import os

print("🤖 Finance Assistant Ready! (Type 'exit' to quit)")

# 🧠 Message history (used as input state)
message_history = []


# 💬 Chat loop
while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break

    message_history.append(HumanMessage(content=user_input))

    # 🚀 Run the LangGraph app
    response = app.invoke({"messages": message_history})

    # Update full history
    message_history = response["messages"]

    # 🧠 Show assistant's last reply
    print("Assistant:", message_history[-1].content)

