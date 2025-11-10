import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
import google.generativeai as genai

# --- 1. SETUP & LOAD .env (HANYA UNTUK FILE INI) ---
# Kita load .env di sini karena file ini butuh API keys
script_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(script_dir, ".env")
load_dotenv(dotenv_path=env_path)

# --- 2. AMBIL KEYS & KONFIGURASI ---
SEARCH_API_KEY = os.getenv('GOOGLE_SEARCH_API_KEY')
SEARCH_ENGINE_ID = os.getenv('SEARCH_ENGINE_ID')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

if not all([SEARCH_API_KEY, SEARCH_ENGINE_ID, GEMINI_API_KEY]):
    print("❌ ERROR (search_engine.py): Pastikan GOOGLE_SEARCH_API_KEY, SEARCH_ENGINE_ID, dan GEMINI_API_KEY ada di .env!")
    # Kita raise error di sini biar bot utama gak jalan
    raise ValueError("Missing critical API keys in .env")

try:
    genai.configure(api_key=GEMINI_API_KEY)
    gemini_model = genai.GenerativeModel('gemini-2.5-flash')
    print("✅ (search_engine.py) Konfigurasi Gemini berhasil.")
except Exception as e:
    print(f"❌ ERROR (search_engine.py): Gagal konfigurasi Gemini. Error: {e}")
    raise

# --- --------------------------------- ---
# --- FUNGSI 1: GOOGLE SEARCH (DARI KODE LAMA) ---
# --- --------------------------------- ---
def get_search_results(query: str) -> list:
    """
    Mengambil 5 hasil pencarian (snippet & link) dari Google Custom Search.
    """
    print(f"🕵️ (search_engine.py) Melakukan pencarian untuk: \"{query}\"")
    try:
        service = build("customsearch", "v1", developerKey=SEARCH_API_KEY)
        res = service.cse().list(
            q=query,
            cx=SEARCH_ENGINE_ID,
            num=5
        ).execute()

        if 'items' not in res:
            print("⚠️ (search_engine.py) Peringatan: Google Search tidak menemukan hasil.")
            return []

        results = []
        for item in res['items']:
            results.append({
                "snippet": item['snippet'].replace('\n', ' ').replace('...', ' '),
                "link": item['link'],
                "title": item['title']
            })
        print(f"✅ (search_engine.py) Google Search menemukan {len(results)} hasil.")
        return results

    except Exception as e:
        print(f"❌ ERROR (search_engine.py) saat search: {e}")
        return []

# --- --------------------------------- ---
# --- FUNGSI 2: RANGKUMAN GEMINI (DARI KODE LAMA) ---
# --- --------------------------------- ---
def get_summary_from_gemini(search_results: list, user_query: str) -> str:
    """
    Mengirim konteks (hasil search) ke Gemini untuk dirangkum.
    """
    print(f"🤖 (search_engine.py) Meminta Gemini untuk merangkum...")
    
    context = ""
    for i, item in enumerate(search_results):
        context += f"Sumber {i+1} ({item['title']}):\n{item['snippet']}\nLink: {item['link']}\n\n"

    prompt = f"""
    Anda adalah seorang analis berita ekonomi yang cerdas.
    Pertanyaan user: "{user_query}"

    Berdasarkan 5 cuplikan berita terbaru di bawah ini, tolong buatkan rangkuman 1-2 paragraf yang menjawab pertanyaan user.
    JANGAN mengarang. Jawaban harus berdasarkan cuplikan di bawah.
    Sertakan juga 2-3 link sumber yang paling relevan di akhir jawabanmu.

    --- CUPLIKAN BERITA ---
    {context}
    --- AKHIR CUPLIKAN ---

    Rangkuman Jawaban Anda:
    """

    try:
        response = gemini_model.generate_content(prompt)
        summary = response.text
        print("✅ (search_engine.py) Gemini berhasil membuat rangkuman.")
        return summary
    except Exception as e:
        print(f"❌ ERROR (search_engine.py) saat generate rangkuman Gemini: {e}")
        return "Maaf, terjadi kesalahan saat saya mencoba merangkum berita."