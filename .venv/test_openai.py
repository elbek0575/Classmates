import os
import openai
from dotenv import load_dotenv

# Загрузка переменных окружения из файла .env
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY должна быть установлена")

openai.api_key = OPENAI_API_KEY

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello, who are you?"}
    ]
)

print(response['choices'][0]['message']['content'])
