import os
import logging
from pyrogram import Client
from config import API_ID, API_HASH, SESSION_STRING
from handlers.command_handler import start_handler
from handlers.download_handler import m3u8_handler

# 📂 Konstanta
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# 📝 Konfigurasi logging
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler("bot.log", encoding="utf-8"),  # Simpan log ke file
        logging.StreamHandler()                            # Tampilkan di console (Colab)
    ]
)
logger = logging.getLogger("M3U8Bot")

# 🚀 Inisialisasi Pyrogram Client
try:
    app = Client("m3u8_userbot", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)
    logger.info("✅ Pyrogram client berhasil dibuat.")
except Exception as e:
    logger.critical(f"❌ Gagal inisialisasi client: {e}")
    raise

# 📌 Daftarkan semua handler
try:
    app.add_handler(start_handler)
    logger.info("📌 Handler /start ditambahkan.")
    
    app.add_handler(m3u8_handler)
    logger.info("📌 Handler download M3U8 ditambahkan.")
except Exception as e:
    logger.error(f"❌ Gagal menambahkan handler: {e}")
    raise

# 🔁 Jalankan UserBot
if __name__ == "__main__":
    logger.info("🚀 M3U8 Downloader Telegram UserBot dimulai...")
    try:
        app.run()
        logger.info("✅ Bot berjalan tanpa error.")
    except Exception as e:
        logger.exception(f"❌ Bot berhenti karena error: {e}")