from typing import TypedDict
import os

from dotenv import load_dotenv

from langchain_openai import ChatOpenAI

from langgraph.graph import StateGraph, END

from langgraph.prebuilt import ToolNode

from app.agent.tools import get_weather


load_dotenv()


class AgentState(TypedDict):

    message: str
    response: str


llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=os.getenv(
        "DEEPSEEK_API_KEY"
    ),
    base_url="https://api.deepseek.com"
)


tools = [
    get_weather
]


llm_with_tools = llm.bind_tools(
    tools
)


def chatbot(state: AgentState):

    result = llm_with_tools.invoke(
        state["message"]
    )

    return {
        "response": result.content
    }


tool_node = ToolNode(
    tools
)


graph_builder = StateGraph(
    AgentState
)


graph_builder.add_node(
    "chatbot",
    chatbot
)


graph_builder.add_node(
    "tools",
    tool_node
)


graph_builder.set_entry_point(
    "chatbot"
)


graph_builder.add_edge(
    "tools",
    "chatbot"
)


graph_builder.add_edge(
    "chatbot",
    END
)


graph = graph_builder.compile()


result = graph.invoke(
    {
        "message":
        "北京天气怎么样？"
    }
)


print(result)