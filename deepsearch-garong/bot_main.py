import discord
import os
from dotenv import load_dotenv
import asyncio
try:
    from agent import ask_gemini_agent
except ImportError:
    print("ERROR: Gagal import ask_gemini_agent dari agent.py.")
    print("Pastikan file ada dan __init__.py ada di foldernya.")
    exit()


TARGET_SERVER_NAME = "ai-deepsearch-agency" 
TARGET_CHANNEL_NAME = "rangkuman-berita-dagang"


# --- Setup ---
script_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(script_dir, ".env")
load_dotenv(dotenv_path=env_path) 

TOKEN = os.getenv('DISCORD_BOT_TOKEN')


intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# --- Event Handler ---
@client.event
async def on_ready():
    """Event ketika bot baru online"""
    print(f'Bot {client.user} online')
    print(f'Hanya akan merespon di Server: "{TARGET_SERVER_NAME}"')
    print(f'Dan di Channel: "{TARGET_CHANNEL_NAME}"')
    print('------')

@client.event
async def on_message(message):
    # FILTER: SELF, SERVER, AND CHANNEL
    if message.author == client.user: 
        return
    if message.guild is None or message.guild.name != TARGET_SERVER_NAME:
        return
    if message.channel.name != TARGET_CHANNEL_NAME:
        return

    
    print(f"Mendapatkan chat di server/channel yang benar: {message.content}")
    
    try:
        await message.channel.send('bleeee')
    except Exception as e:
        print(f"Gagal kirim balasan: {e}")


# --- Run The Bot ---
try:
    print("Mencoba menyalakan bot...")
    client.run(TOKEN)
except discord.errors.LoginFailure:
    print("ERROR: Token bot salah. Pastikan DISCORD_BOT_TOKEN di .env sudah benar.")
except Exception as e:
    print(f"Error aneh terjadi: {e}")



