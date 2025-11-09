import requests
import json
import os
from dotenv import load_dotenv

script_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(script_dir, ".env")
load_dotenv(dotenv_path=env_path) 

DISCORD_URL = os.getenv("DISCORD_WEBHOOK_URL")

if not DISCORD_URL:
    print(f"!!! GAGAL: Tidak bisa menemukan DISCORD_WEBHOOK_URL di {env_path} !!!")


def push_to_discord(rangkuman_riset: str):
    """
    Mengirim rangkuman hasil riset (string) ke channel Discord yang sudah ditentukan.
    """

    if not DISCORD_URL:
        print("--- TOOL ERROR: DISCORD_WEBHOOK_URL tidak ditemukan di .env ---")
        return json.dumps({"status": "gagal", "error": "Discord URL belum di-set"})

    print(f"--- TOOL: Mengirim pesan ke Discord ---")

    data = {
        "content": rangkuman_riset, 
        "username": "kucing garong"   
    }

    try:
        response = requests.post(
            DISCORD_URL, 
            data=json.dumps(data), 
            headers={"Content-Type": "application/json"}
        )

        # 3. Cek status tembakan
        response.raise_for_status() # (Bakal error kalo gagal kirim)

        print("   > Pesan berhasil terkirim ke Discord.")
        return json.dumps({"status": "sukses"})

    except requests.exceptions.RequestException as e:
        print(f"   > ERROR: Gagal ngirim ke Discord: {e}")
        return json.dumps({"status": "gagal", "error": str(e)})

if __name__ == "__main__":
    # Tes 'sanity check'
    print("Menjalankan tes kirim Discord...")
    hasil_tes = push_to_discord("ap")
    print(hasil_tes)
