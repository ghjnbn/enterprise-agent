from typing import TypedDict
import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END


# 加载环境变量
load_dotenv()


# 定义Agent状态
class AgentState(TypedDict):
    message: str
    response: str


# 创建LLM对象
llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)


# Agent节点
def chatbot(state: AgentState):

    # 获取用户输入
    user_message = state["message"]

    # 调用大模型
    result = llm.invoke(
        user_message
    )

    # 返回新的状态
    return {
        "response": result.content
    }


# 创建Graph
graph_builder = StateGraph(AgentState)


# 添加节点
graph_builder.add_node(
    "chatbot",
    chatbot
)


# 设置入口
graph_builder.set_entry_point(
    "chatbot"
)


# 设置结束
graph_builder.add_edge(
    "chatbot",
    END
)


# 编译
graph = graph_builder.compile()


# 运行
result = graph.invoke(
    {
        "message": "请介绍一下什么是AI Agent"
    }
)


print(result)