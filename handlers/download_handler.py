import os
import time
from pyrogram import filters
from pyrogram.types import Message
from pyrogram.handlers import MessageHandler

from utility.video_utils import download_m3u8
from utils.video_meta import get_video_duration, get_thumbnail
from handlers.upload_handler import upload_video

async def handle_m3u8(client, message: Message):
    print("[BOT] 🔗 Menerima link M3U8:", message.text)

    url = message.text.strip()
    await message.reply_text("🔍 Memulai proses unduhan...")

    filename = f"{int(time.time())}.mp4"
    output_path = os.path.join("downloads", filename)

    try:
        await download_m3u8(url, output_path)
        print("[BOT] ✅ Unduhan selesai:", output_path)
        await message.reply_text("✅ Unduhan selesai.")
    except Exception as e:
        await message.reply_text(f"❌ Gagal mengunduh: `{e}`")
        print("[BOT] ❌ Gagal mengunduh:", e)
        return

    await message.reply_text("📤 Memulai upload...")
    print("[BOT] 📤 Siap upload:", output_path)

    duration = get_video_duration(output_path)
    thumb_path = os.path.splitext(output_path)[0] + "_thumb.jpg"
    thumb = get_thumbnail(output_path, thumb_path)

    await upload_video(client, message, output_path, filename, duration, thumb)

# 🎯 Handler Pyrogram
m3u8_handler = MessageHandler(
    handle_m3u8,
    filters.text & ~filters.command("start")
  )
