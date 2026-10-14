from typing import TypedDict, Annotated
import os

from dotenv import load_dotenv

from langchain_openai import ChatOpenAI

from langchain_core.messages import HumanMessage
from langgraph.graph.message import add_messages

from langgraph.graph import StateGraph, END

from langgraph.prebuilt import (
    ToolNode,
    tools_condition
)

from app.agent.tools import get_weather


load_dotenv()


# =====================
# 1. 定义状态
# =====================

class AgentState(TypedDict):

    messages: Annotated[
        list,
        add_messages
    ]


# =====================
# 2. 创建LLM
# =====================

llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=os.getenv(
        "DEEPSEEK_API_KEY"
    ),
    base_url="https://api.deepseek.com"
)


# =====================
# 3. 注册工具
# =====================

tools = [
    get_weather
]


# =====================
# 4. 绑定工具
# =====================

llm_with_tools = llm.bind_tools(
    tools
)


# =====================
# 5. LLM节点
# =====================

def chatbot(state: AgentState):

    response = llm_with_tools.invoke(
        state["messages"]
    )

    return {
        "messages":[response]
    }



# =====================
# 6. Tool节点
# =====================

tool_node = ToolNode(
    tools
)



# =====================
# 7. 创建Graph
# =====================

graph_builder = StateGraph(
    AgentState
)


# 添加LLM节点

graph_builder.add_node(
    "chatbot",
    chatbot
)


# 添加工具节点

graph_builder.add_node(
    "tools",
    tool_node
)



# 设置入口

graph_builder.set_entry_point(
    "chatbot"
)



# 条件判断

graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition
)



# 工具执行后回LLM

graph_builder.add_edge(
    "tools",
    "chatbot"
)



# 编译

graph = graph_builder.compile()



# =====================
# 8.运行
# =====================


result = graph.invoke(
    {
        "messages":[
            HumanMessage(
                content="北京天气怎么样？"
            )
        ]
    }
)


print(result["messages"][-1].content)