
import os
import logging
from pyrogram import Client
from config import API_ID, API_HASH, SESSION_STRING
from handlers.command_handler import start_handler
from handlers.download_handler import m3u8_handler
# from handlers.upload_handler import upload_handler

# 📂 Konstanta
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# 📝 Konfigurasi logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# 🚀 Inisialisasi Pyrogram Client
app = Client("m3u8_userbot", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)

# 📌 Daftarkan semua handler
app.add_handler(start_handler)
app.add_handler(m3u8_handler)
# app.add_handler(upload_handler)

# 🔁 Jalankan UserBot
if __name__ == "__main__":
    logger.info("🚀 M3U8 Downloader Telegram UserBot dimulai...")
    app.run()
