import os
import discord
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get Discord token from environment
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

if not DISCORD_TOKEN:
    print("Error: DISCORD_TOKEN not found in environment variables")
    print("Please create a .env file with your Discord token")
    exit(1)

# Create Discord client
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('!hello'):
        await message.channel.send('Hello! I am your Pokemon growth bot!')

# Run the bot
if __name__ == "__main__":
    client.run(DISCORD_TOKEN)
