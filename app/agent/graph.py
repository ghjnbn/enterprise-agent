from langgraph.graph import StateGraph, END

from app.agent.state import AgentState

from app.agent.nodes import (
    llm_analyze_ticket,
    execute_action
)


builder = StateGraph(AgentState)


builder.add_node(
    "analyze",
    llm_analyze_ticket
)


builder.add_node(
    "execute",
    execute_action
)


builder.set_entry_point(
    "analyze"
)


builder.add_edge(
    "analyze",
    "execute"
)


builder.add_edge(
    "execute",
    END
)


graph = builder.compile()