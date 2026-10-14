from typing import TypedDict
import os

from dotenv import load_dotenv

from langchain_openai import ChatOpenAI

from app.agent.tools import get_weather

from langgraph.graph import StateGraph, END


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



llm_with_tools = llm.bind_tools(
    [
        get_weather
    ]
)



def chatbot(state:AgentState):

    result = llm_with_tools.invoke(
        state["message"]
    )


    return {
        "response": result.content
    }




graph_builder = StateGraph(
    AgentState
)


graph_builder.add_node(
    "chatbot",
    chatbot
)


graph_builder.set_entry_point(
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