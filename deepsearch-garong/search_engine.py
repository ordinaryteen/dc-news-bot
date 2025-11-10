import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
import google.generativeai as genai

# --- 1. SETUP & LOAD .env (HANYA UNTUK FILE INI) ---
script_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(script_dir, ".env")
load_dotenv(dotenv_path=env_path)

# --- 2. AMBIL KEYS & KONFIGURASI ---
SEARCH_API_KEY = os.getenv('GOOGLE_SEARCH_API_KEY')
SEARCH_ENGINE_ID = os.getenv('SEARCH_ENGINE_ID')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

if not all([SEARCH_API_KEY, SEARCH_ENGINE_ID, GEMINI_API_KEY]):
    raise ValueError("Missing critical API keys in .env")

try:
    genai.configure(api_key=GEMINI_API_KEY)
    gemini_model = genai.GenerativeModel('gemini-2.5-flash')
    print("SUKSES: Konfigurasi Gemini berhasil.")
except Exception as e:
    print(f"ERROR: Gagal konfigurasi Gemini. Error: {e}")
    raise

# FUNGSI: SEARCH THE WEB
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
            num=7
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
        print(f"✅ SUKSES Google Search menemukan {len(results)} hasil.")
        return results

    except Exception as e:
        print(f"❌ GAGAL saat search: {e}")
        return []


# FUNGSI: RANGKUMAN GEMINI 
def get_summary_from_gemini(search_results: list, user_query: str) -> str:
    """
    Mengirim konteks (hasil search) ke Gemini untuk dirangkum.
    """

    print(f"Meminta Gemini untuk merangkum...")
    
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
        print(f"✅SUKSES: Gemini berhasil membuat rangkuman.")
        return summary
    except Exception as e:
        print(f"❌ERROR: saat generate rangkuman Gemini: {e}")
        return "Terjadi kesalahan saat merangkum berita."

# FUNGSI: AI GUARDRAIL
def is_query_relevant(user_query: str) -> bool:
    """
    Menggunakan AI untuk mengecek apakah query user RELEVAN dengan topik.
    Ini adalah Panggilan AI #1.
    """
    print(f"🤖 (search_engine.py) Mengecek relevansi topik untuk: \"{user_query}\"")
    
    rule_prompt = f"""
    Aturan Ketat:
    1. Topik yang relevan adalah yang berhubungan LANGSUNG dengan 'perang dagang', 'kebijakan dagang', 'tarif', 'ekspor-impor', atau 'persaingan teknologi' antar negara (terutama Tiongkok dan AS).
    2. Topik TIDAK relevan adalah SEMUA di luar itu (misal: "resep masakan", "ibu kota Prancis", "cara coding", "random chat").

    Pertanyaan User: "{user_query}"

    Berdasarkan aturan di atas, apakah pertanyaan user relevan? Jawab HANYA dengan 'RELEVAN' atau 'TIDAK RELEVAN'.
    """
    
    try:
        response = gemini_model.generate_content(rule_prompt)
        decision = response.text.strip().upper()
        
        print(f"Keputusan AI: {decision}")
        return decision == "RELEVAN"
        
    except Exception as e:
        print(f"❌ ERROR saat cek relevansi: {e}")
        # Kalo error, kita anggep aja relevan biar aman (fail-safe)
        return True