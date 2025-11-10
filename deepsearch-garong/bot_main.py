import discord
import os
import asyncio
from dotenv import load_dotenv

try:
    from search_engine import get_search_results, get_summary_from_gemini
except ImportError:
    print("❌ ERROR: Gagal import 'search_engine.py'.")
    print("Pastikan file 'search_engine.py' ada di folder yang sama.")
    exit()


# --- Setup .env (HANYA UNTUK DISCORD TOKEN) ---
script_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(script_dir, ".env")
load_dotenv(dotenv_path=env_path)

DISCORD_TOKEN = os.getenv('DISCORD_BOT_TOKEN')

if not DISCORD_TOKEN:
    print("❌ ERROR: DISCORD_BOT_TOKEN tidak ditemukan di .env!")
    exit()


TARGET_SERVER_NAME = "ai-deepsearch-agency"
TARGET_CHANNEL_NAME = "rangkuman-berita-dagang"

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


# --- EVENT ON_READY ---
@client.event
async def on_ready():
    print(f'Bot {client.user} online')
    print(f'Hanya akan merespon di Server: "{TARGET_SERVER_NAME}"')
    print(f'Dan di Channel: "{TARGET_CHANNEL_NAME}"')
    print("Ketik '!perangdagang [pertanyaan lo]' untuk memulai.")
    print('------')

# --- EVENT ON_MESSAGE ---
@client.event
async def on_message(message):
    # FILTER: SELF, SERVER, AND CHANNEL
    if message.author == client.user:
        return
    if message.guild is None or message.guild.name != TARGET_SERVER_NAME:
        return
    if message.channel.name != TARGET_CHANNEL_NAME:
        return

    # TRIGGER
    if message.content.startswith('!perangdagang '):
        
        user_query = message.content[len('!perangdagang '):].strip()
        
        if not user_query:
            await message.channel.send("Harap masukkan pertanyaan setelah `!perangdagang `")
            return

        print(f"Mendapatkan command dari {message.author}: {user_query}")
        
        async with message.channel.typing():
            await message.channel.send(f"Oke, `{message.author.display_name}`. Saya lagi cari berita dan bikin rangkuman untuk: \"{user_query}\"...")

            try:
                # --- INI DIA BEDANYA ---
                # 1. Panggil fungsi impor (lebih bersih)
                search_results = get_search_results(user_query) 
                
                if not search_results:
                    await message.channel.send(f"Maaf, saya tidak menemukan artikel berita yang relevan untuk \"{user_query}\".")
                    return

                summary = get_summary_from_gemini(search_results, user_query)

                embed = discord.Embed(
                    title=f"Analisis Perang Dagang: {user_query}",
                    description=summary,
                    color=discord.Color.blue()
                )
                embed.set_footer(text=f"Dirangkum oleh AI | Sumber: Google Search")
                
                await message.channel.send(embed=embed)

            except Exception as e:
                print(f"❌ ERROR di alur utama on_message: {e}")
                await message.channel.send("Waduh, ada error internal. Coba lagi nanti ya.")


# --- Run The Bot ---
try:
    print("Mencoba menyalakan bot...")
    client.run(DISCORD_TOKEN)
except discord.errors.LoginFailure:
    print("ERROR: Token bot salah. Pastikan DISCORD_BOT_TOKEN di .env sudah benar.")
except Exception as e:
    print(f"Error aneh terjadi: {e}")