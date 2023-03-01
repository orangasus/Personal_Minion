# Tasks
# Узнать базу про coroutines


import discord
from discord.ext import commands
import os
import asyncio


api_key_discord = os.environ['DISCORD_TOKEN'] # API key for Discord bot

# Setting discord client
intents = discord.Intents(messages=True, message_content=True,
                          members=True, guilds=True)  # Defining bot permissions/intents
intents = discord.Intents.all()
client = commands.Bot(command_prefix='$', intents=intents,
                      help_command=None)  # Bot initialization

# Setting an array for cogs files
initial_extension = []
for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
    initial_extension.append('cogs.' + filename[:-3])

# Executes once the bot is ready
@client.event
async def on_ready():
  print("--> Personal Minion 2.0 ready to serve")

async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await client.load_extension(f"cogs.{filename[:-3]}")

async def main():
    async with client:
        await load_extensions()
        await client.start(api_key_discord)

asyncio.run(main())