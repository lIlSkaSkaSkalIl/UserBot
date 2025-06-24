import os
import time
from pyrogram.enums import ParseMode
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

    # 🔒 Cegah unduhan ganda
    if global_download_lock.locked():
        await message.reply_text("⏳ Maaf, sedang ada unduhan aktif. Mohon tunggu hingga selesai.")
        return

    async with global_download_lock:
        start_time = time.time()
        status_msg = await message.reply_text("🔍 Memulai proses unduhan...")

        filename = f"{int(start_time)}.mp4"
        output_path = os.path.join("downloads", filename)

        # 📥 Callback progres unduhan
        async def progress_callback(size_mb):
            elapsed = time.time() - start_time
            speed = size_mb / elapsed if elapsed > 0 else 0

            text = (
                "<pre>\n"
                "╔════════════════════════════════╗\n"
                "  🚀 Progres Unduhan Aktif\n"
                "╠════════════════════════════════╣\n\n"
                f" 📂 Nama File     : {filename}\n"
                f" 🔗 URL Sumber    : {url}\n"
                f" 📦 Ukuran Terunduh: {size_mb:.2f} MB\n"
                f" ⏱️ Waktu Berlalu : {elapsed:.1f} detik\n"
                f" 🚀 Kecepatan     : {speed:.2f} MB/s\n\n"
                "╚════════════════════════════════╝\n"
                "</pre>"
            )
            try:
                await status_msg.edit_text(text, parse_mode=ParseMode.HTML)
            except Exception:
                pass  # Biarkan error edit jika rate limit

        # 🚀 Proses unduhan
        try:
            await download_m3u8(url, output_path, progress_callback)
            print("[BOT] ✅ Unduhan selesai:", output_path)
            await status_msg.edit_text("✅ Unduhan selesai.")
        except Exception as e:
            await status_msg.edit_text(f"❌ Gagal mengunduh: `{e}`")
            return

        # 📤 Proses unggah
        await message.reply_text("📤 Memulai proses upload...")
        print("[BOT] 📤 Siap upload:", output_path)

        duration = get_video_duration(output_path)
        thumb_path = os.path.splitext(output_path)[0] + "_thumb.jpg"
        thumb = get_thumbnail(output_path, thumb_path)

        await upload_video(client, message, output_path, filename, duration, thumb)

        # 🧹 Bersihkan file lokal
        if os.path.exists(output_path):
            os.remove(output_path)

# ✅ Handler utama
m3u8_handler = MessageHandler(
    handle_m3u8,
    filters.text & ~filters.command("start")
)
