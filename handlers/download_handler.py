import os
import time
from pyrogram import filters
from pyrogram.types import Message
from pyrogram.handlers import MessageHandler
from pyrogram.enums import ParseMode  # ✅ Import enum parse mode

from utility.video_utils import download_m3u8
from utils.video_meta import get_video_duration, get_thumbnail
from handlers.upload_handler import upload_video
from utils.download_lock import global_download_lock

async def handle_m3u8(client, message: Message):
    url = message.text.strip()
    print("[BOT] 🔗 Link M3U8 diterima:", url)

    # 🔒 Cek apakah ada unduhan aktif
    if global_download_lock.locked():
        await message.reply_text(
            "⏳ Maaf, sedang ada unduhan aktif. Mohon tunggu hingga selesai.",
            parse_mode=ParseMode.HTML  # ✅ HTML enum parse mode
        )
        return

    async with global_download_lock:
        # ✅ Tes parse_mode=HTML dengan teks statis
        await message.reply_text(
            "<b>🔧 Tes ParseMode HTML berhasil!</b>\n<i>Ini teks miring</i>\n<code>Ini kode</code>",
            parse_mode=ParseMode.HTML  # ✅ Gunakan enum, bukan string
        )

        status_msg = await message.reply_text("🔍 Memulai proses unduhan...")

        start_time = time.time()
        filename = f"{int(start_time)}.mp4"
        output_path = os.path.join("downloads", filename)

        # Callback progres unduhan
        async def progress_callback(size_mb):
            elapsed = time.time() - start_time
            speed = size_mb / elapsed if elapsed > 0 else 0

            text = (
                "<b>📥 Sedang mengunduh...</b>\n\n"
                f"<b>Nama file:</b> <code>{filename}</code>\n"
                f"<b>URL:</b> <code>{url}</code>\n"
                f"<b>Terunduh:</b> <code>{size_mb:.2f} MB</code>\n"
                f"<b>Waktu:</b> <code>{elapsed:.1f} detik</code>\n"
                f"<b>Kecepatan:</b> <code>{speed:.2f} MB/s</code>"
            )
            try:
                await status_msg.edit_text(text, parse_mode=ParseMode.HTML)
            except:
                pass  # Abaikan jika gagal update

        try:
            await download_m3u8(url, output_path, progress_callback)
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

# ✅ Pasang handler
m3u8_handler = MessageHandler(
    handle_m3u8,
    filters.text & ~filters.command("start")
            )
