from langgraph.graph import (
    StateGraph,
    END
)

from langgraph.prebuilt import (
    ToolNode,
    tools_condition
)


from app.agent.state import AgentState

from app.agent.nodes import chatbot

from app.agent.tools import get_weather



# 注册工具

tools = [
    get_weather
]


# 创建ToolNode

tool_node = ToolNode(
    tools
)



# 创建Graph

graph_builder = StateGraph(
    AgentState
)



# 添加LLM节点

graph_builder.add_node(
    "chatbot",
    chatbot
)



# 添加Tool节点

graph_builder.add_node(
    "tools",
    tool_node
)



# 设置入口

graph_builder.set_entry_point(
    "chatbot"
)



# 条件边

graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition
)



# 工具执行后返回LLM

graph_builder.add_edge(
    "tools",
    "chatbot"
)



# 编译

graph = graph_builder.compile()