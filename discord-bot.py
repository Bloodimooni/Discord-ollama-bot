import os
import sys

try:
    import discord
    import requests
    from dotenv import load_dotenv

except:
    os.popen("pip install discord.py requests python-dotenv")
    os.popen("apt install python3-discord.py python3-requests python3-dotenv")

    import discord
    import requests
    from dotenv import load_dotenv


load_dotenv()
START = ".chat"
TOKEN = os.getenv("TOKEN")


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

def send_to_ollama(message):
    
    url = "http://localhost:11434/api/generate"

    data = {
        "model":"llama2-uncensored",
        "prompt": message
    }

    try: 
        response = requests.post(url, json=data)
        response.raise_for_status()

        answer = response.json().get("answer", "Sorry, I could not process that.")

        return answer

    except requests.exceptions.RequestException as e:

        return f"An error occured: {e}"


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith(START):
        ollama_response = send_to_ollama(message.content[len(START):])
        await message.channel.send(ollama_response)

    
client.run(TOKEN)