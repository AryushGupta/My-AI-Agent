# Current chat memory
messages = [
    {
        "role": "system",
        "content": "You are a helpful assistant."
    }
]

def add_message(role, content):
    messages.append({
        "role":role,
        "content":content
    })

def get_chat_memory():
    return messages