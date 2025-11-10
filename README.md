# 🐱 Kucing Garong - Bot Analis Berita AI

**Kucing Garong** adalah bot Discord yang ditenagai AI (Google Gemini & Google Search) yang berfungsi sebagai asisten riset spesialis. Bot ini memonitor, mengekstrak, dan merangkum berita *real-time* dari web mengenai topik spesifik (perang dagang AS-China) dan menyajikannya dengan persona kucing yang imut.

---

### 🚀 Video Demo
![Video Demo Kucing Garong](https://github.com/user-attachments/assets/b82c93d4-1375-4835-8c21-1478189fc930)

---

### ✨ Fitur Utama

* **Retrieval-Augmented Generation (RAG):** Mengimplementasikan alur RAG kustom. Bot akan **Mengambil (Retrieve)** data *live* dari Google Search, lalu **Menambahkan (Augment)** data itu sebagai konteks ke AI untuk **Menghasilkan (Generate)** rangkuman.
* **AI-Powered Summarization:** Menggunakan model **Google Gemini 1.5 Flash** untuk merangkum berbagai *snippet* berita menjadi satu paragraf jawaban yang koheren.
* **Real-Time Web Search:** Terhubung dengan **Google Custom Search (CSE) API** untuk mendapatkan hasil pencarian yang relevan dan *up-to-date*.
* **AI Guardrail (Filter Topik):** Menggunakan panggilan AI *pre-processing* untuk mengklasifikasikan intensi user. Bot akan **menolak** pertanyaan yang *off-topic*.
* **Persona Kustom:** Ditenagai oleh *prompt engineering* untuk memberikan semua jawaban dengan persona "Kucing Garong".
* **Aman & Modular:** Kode diorganisir secara modular (logika bot vs logika *engine*) dan semua *secret key* diamankan menggunakan `.env` dan `.gitignore`.

---

### 🔧 Tumpukan Teknologi (Tech Stack)

* **Bahasa:** Python
* **Key Libraries:**
    * `discord.py` (Discord Bot API)
    * `google-generativeai` (Gemini API)
    * `google-api-python-client` (Google Custom Search API)
    * `python-dotenv` (Manajemen Environment)

---

### 🛠️ Cara Instalasi & Menjalankan

Proyek ini **AMAN** untuk di-publikasikan. Semua *key* rahasia disimpan di file `.env` yang di-abaikan oleh `.gitignore`.

Jika Anda ingin menjalankan bot ini di server Anda sendiri, ikuti langkah-langkah ini:

#### 1. Clone Repository

```bash
git clone [https://github.com/](https://github.com/)[USERNAME-LO]/[REPO-NAME-LO].git
cd [REPO-NAME-LO]
```
#### 2.Buat & Aktifkan Virtual Environment

```bash
# Buat venv
python3 -m venv .venv

# Aktifkan di Linux/macOS
source .venv/bin/activate

# Aktifkan di Windows (PowerShell)
# .\.venv\Scripts\Activate.ps1
```

#### 3. Instal Dependensi
```bash
pip install -r requirements.txt
```

#### 4. Buat File .env (Paling Penting)
Buat file baru bernama .env di dalam folder deepsearch-garong/. Salin template di bawah ini dan isi dengan secret key Anda

```bash
# Dapatkan dari Discord Developer Portal
DISCORD_BOT_TOKEN=TOKEN_BOT_DISCORD_ANDA

# Dapatkan dari Google AI Studio (https://aistudio.google.com/app/apikey)
GEMINI_API_KEY=API_KEY_GEMINI_ANDA

# Dapatkan dari Google Cloud Console (https://console.cloud.google.com/apis/credentials)
GOOGLE_SEARCH_API_KEY=API_KEY_GOOGLE_SEARCH_ANDA

# Dapatkan dari Google Programmable Search Engine (https://programmablesearchengine.google.com/)
# Anda harus membuat Search Engine baru dan mengarahkannya ke situs web (misal: reuters.com, bloomberg.com)
SEARCH_ENGINE_ID=ID_SEARCH_ENGINE_ANDA
```

#### 5. Jalankan Bot
Setelah semua key terisi, jalankan file bot_main.py:

```bash
python deepsearch-garong/bot_main.py
```
