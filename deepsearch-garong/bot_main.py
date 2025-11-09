import discord
import os
from dotenv import load_dotenv

# --- Setup ---
script_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(script_dir, ".env")
load_dotenv(dotenv_path=env_path) 

TOKEN = os.getenv('DISCORD_BOT_TOKEN')

if not TOKEN:
    print("ERROR: DISCORD_BOT_TOKEN tidak ditemukan di .env")
    exit()
else:
    print(f'SUCCES: DISCORD_BOT_TOKEN ditemukan: {TOKEN[:4]}')





