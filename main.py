from langgraph.graph import StateGraph, START, END

from agents.state import QEState
from agents.planner import planner
from agents.generator import generator
from agents.executor import executor
from agents.triager import triager


builder = StateGraph(QEState)

builder.add_node("planner", planner)
builder.add_node("generator", generator)
builder.add_node("executor", executor)
builder.add_node("triager", triager)

builder.add_edge(START, "planner")
builder.add_edge("planner", "generator")
builder.add_edge("generator", "executor")
builder.add_edge("executor", "triager")
builder.add_edge("triager", END)

graph = builder.compile()


state = {
    "spec": """
POST /pet

Create a new pet

Request Body

{
   "id": integer,
   "name": string,
   "status": "available|pending|sold"
}
""",
    "test_plan": {},
    "generated_test_file": "",
    "execution_result": {},
    "bug_report": {}
}

result = graph.invoke(state)

print("\n========== FINAL BUG REPORT ==========\n")
print(result["bug_report"])