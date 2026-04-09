from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, END
from agents.workers import WorkerAgents
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], "The conversation history"]

# Define the Workflow
workflow = StateGraph(AgentState)
workers = WorkerAgents()

# Add Nodes
workflow.add_node("researcher", workers.researcher)
workflow.add_node("analyst", workers.analyst)

# Define Logic (Research -> then Analyze)
workflow.set_entry_point("researcher")
workflow.add_edge("researcher", "analyst")
workflow.add_edge("analyst", END)

app = workflow.compile()

if __name__ == "__main__":
    print("--- Multi-Agent Orchestrator Initialized ---")
    # Example Trigger
    # inputs = {"messages": [HumanMessage(content="Analyze the impact of GenAI on retail.")]}
    # app.invoke(inputs)
