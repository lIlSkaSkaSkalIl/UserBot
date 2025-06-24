import os
import time
from pyrogram import filters
from pyrogram.types import Message
from pyrogram.handlers import MessageHandler

from utility.video_utils import download_m3u8
from utils.video_meta import get_video_duration, get_thumbnail
from handlers.upload_handler import upload_video
from utils.download_lock import global_download_lock  # ✅ Import lock

async def handle_m3u8(client, message: Message):
    url = message.text.strip()
    print("[BOT] 🔗 Link M3U8 diterima:", url)

    # 🔒 Cegah unduhan ganda
    if global_download_lock.locked():
        await message.reply_text("⏳ Maaf, sedang ada unduhan aktif. Mohon tunggu hingga selesai.")
        return

    async with global_download_lock:
        filename = f"{int(time.time())}.mp4"
        output_path = os.path.join("downloads", filename)

        try:
            # ⏬ Unduh dengan progres ke Telegram
            await download_m3u8(url, output_path, message)
            print("[BOT] ✅ Unduhan selesai:", output_path)
            await message.reply_text("✅ Unduhan selesai.")
        except Exception as e:
            await message.reply_text(f"❌ Gagal mengunduh: `{e}`")
            return

        await message.reply_text("📤 Memulai proses upload...")
        print("[BOT] 📤 Siap upload:", output_path)

        # 🎞️ Ambil metadata
        duration = get_video_duration(output_path)
        thumb_path = os.path.splitext(output_path)[0] + "_thumb.jpg"
        thumb = get_thumbnail(output_path, thumb_path)

        # 🚀 Upload ke Telegram
        await upload_video(client, message, output_path, filename, duration, thumb)

        # 🧹 Bersihkan video setelah upload
        if os.path.exists(output_path):
            os.remove(output_path)

# 🔌 Registrasi handler
m3u8_handler = MessageHandler(
    handle_m3u8,
    filters.text & ~filters.command("start")
)
