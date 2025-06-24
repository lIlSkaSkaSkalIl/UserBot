import os
from pyrogram import Client, filters
from config import API_ID, API_HASH, SESSION_STRING
from handlers.command_handler import start_handler
from handlers.download_handler import m3u8_handler

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

app = Client("m3u8_userbot", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)

# ✅ Tambahkan handler
app.add_handler(start_handler)
app.add_handler(m3u8_handler)

if __name__ == "__main__":
    print("🚀 UserBot dimulai...")
    app.run()
