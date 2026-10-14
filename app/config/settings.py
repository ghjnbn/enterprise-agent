import os

from dotenv import load_dotenv


load_dotenv()


DEEPSEEK_API_KEY = os.getenv(
    "DEEPSEEK_API_KEY"
)


MODEL_NAME = "deepseek-chat"


BASE_URL = "https://api.deepseek.com"