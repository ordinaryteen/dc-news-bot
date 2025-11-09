import os
from dotenv import load_dotenv
from googleapiclient.discovery import build

# --- 1. SETUP & LOAD .env ---
print("Menjalankan Google Custom Search Test...")
script_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(script_dir, ".env")
load_dotenv(dotenv_path=env_path)


# --- 2. AMBIL KEY DARI .env ---
API_KEY = os.getenv('GOOGLE_SEARCH_API_KEY')
SEARCH_ENGINE_ID = os.getenv('SEARCH_ENGINE_ID')


if not all([API_KEY, SEARCH_ENGINE_ID]):
    print("❌ ERROR: Pastikan GOOGLE_SEARCH_API_KEY dan SEARCH_ENGINE_ID ada di .env!")
    exit()

# --- 3. SIAPKAN PERTANYAAN ---
TEST_QUERY = "US China trade war"

def jalankan_custom_search(query):
    try:
        # --- 4. BUAT KLIEN ---
        service = build("customsearch", "v1", developerKey=API_KEY)

        print(f"📡 Menghubungi Google Custom Search (ID: {SEARCH_ENGINE_ID})...")
        print(f"Mengirim pertanyaan: \"{query}\"")

        # --- 5. KIRIM API CALL ---
        res = service.cse().list(
            q=query,
            cx=SEARCH_ENGINE_ID,
            num=5 
        ).execute()

        # --- 6. TAMPILKAN HASIL ---
        if 'items' in res:
            print("\n✅--- HASIL PENCARIAN ---")
            for i, item in enumerate(res['items']):
                print(f"  {i+1}. {item['title']}")
                print(f"     Link: {item['link']}")
                print(f"     Cuplikan: {item['snippet'].replace('...', '')}\n")
        else:
            print("\n❌--- GAGAL: Tidak ada hasil ditemukan. ---")
            print("Pastikan SEARCH_ENGINE_ID lo udah di-setup di web Google CSE")
            print("untuk nyari di Reuters & Bloomberg.")

    except Exception as e:
        print(f"\n❌--- GAGAL ---")
        print(f"Error: {e}")
        print("\n--- KEMUNGKINAN PENYEBAB ---")
        print("1. GOOGLE_SEARCH_API_KEY lo salah / belum di-enable.")
        print("2. SEARCH_ENGINE_ID lo salah.")

# --- Jalankan fungsi utama ---
if __name__ == "__main__":
    jalankan_custom_search(TEST_QUERY)