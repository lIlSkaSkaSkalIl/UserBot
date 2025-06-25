import os
import time
import logging
from pyrogram import filters
from pyrogram.enums import ParseMode
from pyrogram.types import Message
from pyrogram.handlers import MessageHandler

from utils.video_utils import download_m3u8
from utils.video_meta import get_video_duration, get_thumbnail
from handlers.upload_handler import upload_video
from utils.download_lock import global_download_lock

logger = logging.getLogger(__name__)

async def handle_m3u8(client, message: Message) -> None:
    """
    Handler untuk menangani pesan berisi link M3U8 dan melakukan download.
    """
    url = message.text.strip()
    logger.info("🔗 Link M3U8 diterima dari user %s: %s", message.from_user.id, url)
    print(f"🔗 Link diterima: {url}")

    if global_download_lock.locked():
        await message.reply_text("⏳ Maaf, sedang ada unduhan aktif. Mohon tunggu hingga selesai.")
        return

    async with global_download_lock:
        start_time = time.time()
        status_msg = await message.reply_text("🔍 Memulai proses unduhan...")

        filename = f"{int(start_time)}.mp4"
        output_path = os.path.join("downloads", filename)
        ext = os.path.splitext(output_path)[1]

        last_update_time = 0

        async def progress_callback(size_mb: float) -> None:
            nonlocal last_update_time
            now = time.time()
            if now - last_update_time < 10:
                return
            last_update_time = now

            elapsed = now - start_time
            speed = size_mb / elapsed if elapsed > 0 else 0

            text = (
                "   <b>📥 Progres Download</b>\n\n"
                "╭━━━━━━━━━━━━━━━━━━━━━╮\n"
                f" 📝 <b>Nama:</b> <code>{filename}</code>\n"
                f" 📂 <b>Ekstensi:</b> <code>{ext}</code>\n"
                f" 📦 <b>Terunduh:</b> <code>{size_mb:.2f} MB</code>\n"
                f" ⏱️ <b>Waktu:</b> <code>{elapsed:.1f} detik</code>\n"
                f" 🚀 <b>Kecepatan:</b> <code>{speed:.2f} MB/s</code>\n"
                "╰━━━━━━━━━━━━━━━━━━━━━╯"
            )

            try:
                await status_msg.edit_text(text, parse_mode=ParseMode.HTML)
            except Exception as e:
                logger.warning("Gagal update progres: %s", e)

        try:
            await download_m3u8(url, output_path, progress_callback)
            logger.info("✅ Unduhan selesai: %s", output_path)
            print("✅ Unduhan selesai, memulai validasi file...")
            await status_msg.edit_text("✅ Unduhan selesai.")
        except Exception as e:
            logger.error("❌ Gagal mengunduh: %s", e)
            await status_msg.edit_text(f"❌ Gagal mengunduh: <code>{e}</code>", parse_mode=ParseMode.HTML)
            return

        # Validasi file
        print("🔎 Memvalidasi file hasil unduhan...")
        logger.info("🔎 Memvalidasi file hasil unduhan...")

        if not os.path.exists(output_path):
            await message.reply_text("❌ File tidak ditemukan setelah unduhan.")
            logger.error("❌ File tidak ditemukan setelah unduhan.")
            return

        logger.info("✅ Validasi selesai. File ditemukan.")
        print("✅ Validasi selesai. File ditemukan.")

        # Upload
        await message.reply_text("📤 Memulai proses upload...")
        logger.info("📤 Mengunggah: %s", output_path)
        print("📤 Upload ke Telegram dimulai...")

        logger.info("🎬 Mengambil metadata video...")
        print("🎬 Mengambil metadata video...")
        duration = get_video_duration(output_path)
        
        logger.info("🖼️ Menghasilkan thumbnail...")
        print("🖼️ Membuat thumbnail...")
        thumb_path = os.path.splitext(output_path)[0] + "_thumb.jpg"
        thumb = get_thumbnail(output_path, thumb_path)

        logger.info("📤 Mengunggah video ke Telegram...")
        print("📤 Mengunggah video ke Telegram...")

        await upload_video(client, message, output_path, filename, duration, thumb)

        if os.path.exists(output_path):
            os.remove(output_path)

# Handler Pyrogram
m3u8_handler = MessageHandler(handle_m3u8, filters.text & ~filters.command("start"))
