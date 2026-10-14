import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI


# 加载 .env
load_dotenv()


# 创建模型
llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)


# 发送消息
response = llm.invoke(
    "你好，请介绍一下你自己"
)


print(response.content)