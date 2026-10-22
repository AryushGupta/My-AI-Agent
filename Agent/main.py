# using groq to build an AI Agent
import os
from dotenv import load_dotenv
from groq import Groq
from Agent.memory import get_chat_memory, add_message

load_dotenv()

client = Groq(
    api_key=os.getenv("GROK_API_KEY")
    )

# try to change the purpose of this llm in next step
def response_to_user(message : str) -> str :

    ''' client (Groq client object) -> chat(groups chat -related functionalty) -> completions(provides chat-completion functionality) -> create(submits your request to generate a response) '''

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": message,
            }
        ],
        model="openai/gpt-oss-120b",
    )
    add_message("system", chat_completion.choices[0].message.content)
    return chat_completion.choices[0].message.content

print("What are you building today?")

while True:
    user_ip = input()
    add_message("user", user_ip)

    if user_ip.lower() == "exit":
        add_message("user", user_ip.lower())
        add_message("system","Thank you for chatting!")
        break

    print(response_to_user(user_ip))

# add_message("user","hello")
# add_message("system","Hi!!!")

print(get_chat_memory())