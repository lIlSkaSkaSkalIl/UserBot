import os
import time
from datetime import datetime
from pyrogram import filters
from pyrogram.types import Message
from pyrogram.handlers import MessageHandler

from utility.video_utils import download_m3u8
from utils.video_meta import get_video_duration, get_thumbnail, get_video_info
from handlers.upload_handler import upload_video
from utils.download_lock import global_download_lock

async def handle_m3u8(client, message: Message):
    url = message.text.strip()
    print("[BOT] 🔗 Link M3U8 diterima:", url)

    if global_download_lock.locked():
        await message.reply_text("⏳ Maaf, sedang ada unduhan aktif. Mohon tunggu hingga selesai.")
        return

    async with global_download_lock:
        start_time = time.time()
        status_msg = await message.reply_text("🔍 Memulai proses unduhan...")

        filename = f"{int(start_time)}.mp4"
        output_path = os.path.join("downloads", filename)

        info_cache = {}

        # Callback progres unduhan (diperbarui tiap 10 detik)
        async def progress_callback(size_mb):
            elapsed = time.time() - start_time
            speed = size_mb / elapsed if elapsed > 0 else 0
            time_now = datetime.now().strftime("%d %b %Y %H:%M:%S")
            ext = os.path.splitext(output_path)[1]

            width = info_cache.get("width", "-")
            height = info_cache.get("height", "-")
            codec = info_cache.get("codec", "-")

            text = (
                "📥 <b>Progres Unduhan</b>\n\n"
                "━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"📝 <b>Nama File:</b> <code>{filename}</code>\n"
                f"📁 <b>Ekstensi:</b> <code>{ext}</code>\n"
                f"📏 <b>Resolusi:</b> <code>{width}x{height}</code>\n"
                f"🎞️ <b>Codec:</b> <code>{codec}</code>\n"
                f"🔗 <b>URL:</b> <code>{url}</code>\n"
                f"⬇️ <b>Terunduh:</b> <code>{size_mb:.2f} MB</code>\n"
                f"⏱️ <b>Durasi:</b> <code>{elapsed:.1f} detik</code>\n"
                f"⚡ <b>Kecepatan:</b> <code>{speed:.2f} MB/s</code>\n"
                f"🕓 <b>Waktu:</b> <code>{time_now}</code>\n"
                "━━━━━━━━━━━━━━━━━━━━━━━"
            )
            try:
                await status_msg.edit_text(text, parse_mode="html")
            except:
                pass  # Biarkan jika gagal edit (misal rate limit)

        try:
            await download_m3u8(url, output_path, progress_callback)

            # Ambil metadata setelah video selesai diunduh
            info_cache.update(get_video_info(output_path))

            print("[BOT] ✅ Unduhan selesai:", output_path)
            await status_msg.edit_text("✅ Unduhan selesai.")
        except Exception as e:
            await status_msg.edit_text(f"❌ Gagal mengunduh: `{e}`")
            return

        await message.reply_text("📤 Memulai proses upload...")
        print("[BOT] 📤 Siap upload:", output_path)

        duration = get_video_duration(output_path)
        thumb_path = os.path.splitext(output_path)[0] + "_thumb.jpg"
        thumb = get_thumbnail(output_path, thumb_path)

        await upload_video(client, message, output_path, filename, duration, thumb)

        if os.path.exists(output_path):
            os.remove(output_path)

m3u8_handler = MessageHandler(
    handle_m3u8,
    filters.text & ~filters.command("start")
)
