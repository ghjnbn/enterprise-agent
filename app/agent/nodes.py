from langchain_openai import ChatOpenAI

from app.agent.state import AgentState
from app.agent.tools import get_weather

from app.config.settings import (
    DEEPSEEK_API_KEY,
    MODEL_NAME,
    BASE_URL
)


llm = ChatOpenAI(
    model=MODEL_NAME,
    api_key=DEEPSEEK_API_KEY,
    base_url=BASE_URL
)


tools=[
    get_weather
]


llm_with_tools = llm.bind_tools(
    tools
)


def chatbot(state: AgentState):

    response = llm_with_tools.invoke(
        state["messages"]
    )

    return {
        "messages":[response]
    }