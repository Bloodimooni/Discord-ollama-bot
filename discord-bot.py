import os
import discord
import requests
from dotenv import load_dotenv
import json

load_dotenv()
START = ".chat"
TOKEN = os.getenv("TOKEN")


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

async def ask_ollama(question,model="llama2-uncensored"):

    if "code" in question:
        print("Using codellama to answer")
        url = 'http://localhost:11434/api/generate'
        data = {"model": "codellama", "prompt": question}

    else:
        print(f"using {model} to answer")
        url = 'http://localhost:11434/api/generate'
        data = {"model": model, "prompt": question}

    try:
        response = requests.post(url, json=data)
        response.raise_for_status()

        # Split the response into individual JSON strings
        json_strings = response.text.strip().split('\n')

        # Parse each JSON string and concatenate the 'response' fields
        full_response = ''
        for json_str in json_strings:
            parsed_json = json.loads(json_str)
            full_response += parsed_json.get('response', '')

        return full_response

    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"
    except json.JSONDecodeError as e:
        return f"JSON parsing error: {e}"


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith(START):
        ollama_response = await ask_ollama(message.content[len(START):])
        await message.channel.send(ollama_response)

    if message.content.startswith(START + "-mistral"):
        ollama_response = await ask_ollama(message.content[len(START + "-mistral"):],model="mistral")
        await message.channel.send(ollama_response)

client.run(TOKEN)