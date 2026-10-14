from langchain_openai import ChatOpenAI

from app.config.settings import (
    DEEPSEEK_API_KEY,
    DEEPSEEK_BASE_URL
)


llm = ChatOpenAI(

    model="deepseek-chat",

    api_key=DEEPSEEK_API_KEY,

    base_url=DEEPSEEK_BASE_URL,

    temperature=0

)