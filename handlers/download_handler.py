import os
import time
import html  # Untuk menghindari karakter HTML tidak valid
from pyrogram import filters
from pyrogram.types import Message
from pyrogram.handlers import MessageHandler

from utility.video_utils import download_m3u8
from utils.video_meta import get_video_duration, get_thumbnail
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

        # ✅ Callback progres (setiap 10 detik)
        async def progress_callback(size_mb):
            elapsed = time.time() - start_time
            speed = size_mb / elapsed if elapsed > 0 else 0

            text = (
                "<b>📥 Sedang mengunduh...</b>\n\n"
                f"<b>📄 Nama file:</b> <code>{html.escape(filename)}</code>\n"
                f"<b>🔗 URL:</b> <code>{html.escape(url)}</code>\n"
                f"<b>⏱️ Waktu:</b> <code>{elapsed:.1f} detik</code>\n"
                f"<b>🚀 Kecepatan:</b> <code>{speed:.2f} MB/s</code>\n"
                f"<b>📦 Terunduh:</b> <code>{size_mb:.2f} MB</code>"
            )
            try:
                await status_msg.edit_text(text, parse_mode="html")
            except Exception as e:
                print(f"[!] Gagal update pesan: {e}")

        # 🚀 Mulai unduh
        try:
            await download_m3u8(url, output_path, progress_callback)
            print("[BOT] ✅ Unduhan selesai:", output_path)
            await status_msg.edit_text("✅ Unduhan selesai.")
        except Exception as e:
            await status_msg.edit_text(f"❌ Gagal mengunduh: <code>{html.escape(str(e))}</code>", parse_mode="html")
            return

        await message.reply_text("📤 Memulai proses upload...")
        print("[BOT] 📤 Siap upload:", output_path)

        duration = get_video_duration(output_path)
        thumb_path = os.path.splitext(output_path)[0] + "_thumb.jpg"
        thumb = get_thumbnail(output_path, thumb_path)

        await upload_video(client, message, output_path, filename, duration, thumb)

        if os.path.exists(output_path):
            os.remove(output_path)

# ✅ Handler
m3u8_handler = MessageHandler(
    handle_m3u8,
    filters.text & ~filters.command("start")
)
