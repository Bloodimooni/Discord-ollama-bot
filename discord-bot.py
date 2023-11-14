import os
import discord
import requests
from dotenv import load_dotenv
import json

load_dotenv()
START = ".chat"
TOKEN = os.getenv("TOKEN")

LIST_OF_MODELS = ["llama2-uncensored","codellama","mistral"]
MODEL = LIST_OF_MODELS[0]

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

async def ask_ollama(question):

    if "code" in question:
        print("[!]\tUSED MODEL OVERRIDE, USING CODELLAMA FOR THIS PROMPT.")
        url = 'http://localhost:11434/api/generate'
        data = {"model": "codellama", "prompt": question}

    else:
        url = 'http://localhost:11434/api/generate'
        data = {"model": MODEL, "prompt": question}

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

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith(START + " list"):
        await message.channel.send("You can choose between different models:\
                                   \n\t- llama2-uncensored (default)\
                                   \n\t- coding model (Just type 'code' in the prompt)\
                                   \n\t- Mistral (A chatgpt like Model)")
        await message.channel.send("Just type [.chat select model] to use for your next prompt.")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith(START + " select "):
        model = message.content[len(START + " select "):]
        if model.lower() in LIST_OF_MODELS:
            MODEL = model
        else:
            await message.channel.send(f"I am sorry, but I don't have the model: {model}\nI can only use the following: {LIST_OF_MODELS}.")
    
client.run(TOKEN)