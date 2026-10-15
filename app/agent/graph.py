from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from app.agent.state import AgentState
from app.agent.nodes import (
    llm_analyze_ticket,
    call_tool_agent
)
from app.agent.tools import check_service, restart_service


# 注册可供 ToolNode 执行的工具。
tools = [check_service, restart_service]

builder = StateGraph(AgentState)

builder.add_node(
    "analyze",
    llm_analyze_ticket
)

builder.add_node(
    "agent",
    call_tool_agent
)

builder.add_node(
    "tools",
    ToolNode(tools)
)

builder.set_entry_point("analyze")

builder.add_edge(
    "analyze",
    "agent"
)

# 模型发出工具调用时进入 tools；否则结束工作流。
builder.add_conditional_edges(
    "agent",
    tools_condition
)

# 工具执行完成后回到模型，让模型读取工具结果。
builder.add_edge(
    "tools",
    "agent"
)

graph = builder.compile()