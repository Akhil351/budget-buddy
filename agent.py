# 📁 agent.py

from typing import Annotated, Sequence, TypedDict
from dotenv import load_dotenv
import os

from langchain_core.messages import BaseMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

# ✅ Import tools
from tools import add_income, add_expense, get_balance, get_total_income, get_total_expense,get_today_date

# ✅ Load environment variables from `.env`
load_dotenv()

# ✅ Available tools for the agent
tools = [add_income, add_expense, get_balance, get_total_income, get_total_expense,get_today_date]

# ✅ Define state passed through the graph
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

# ✅ Initialize OpenAI model with tools bound
model = ChatOpenAI(
    model="gpt-4o",
    api_key=os.getenv("OPENAI_API_KEY") # type: ignore
).bind_tools(tools)

# ✅ Agent node: combines system message + user messages, gets AI response
def model_call(state: AgentState) -> AgentState:
    system_prompt = SystemMessage(
        content="You are a finance assistant that helps users track income, expenses, and balances."
    )
    response = model.invoke([system_prompt] + state["messages"]) # type: ignore
    return {"messages": [response]}

# ✅ Conditional logic: check if tool call is needed
def should_continue(state: AgentState):
    last_message = state["messages"][-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls: # type: ignore
        return "continue"
    return "end"

# ✅ Build LangGraph with agent + tool node + control flow
graph = StateGraph(AgentState)
graph.add_node("agent", model_call)
graph.add_node("tools", ToolNode(tools=tools))
graph.add_edge(START, "agent")
graph.add_conditional_edges("agent", should_continue, {
    "continue": "tools",
    "end": END
})
graph.add_edge("tools", "agent")

# ✅ Compile to get executable app
app = graph.compile()
