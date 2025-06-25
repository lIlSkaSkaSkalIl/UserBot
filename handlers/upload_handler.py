import os
import time
import logging
from pyrogram.types import Message
from pyrogram import Client
from pyrogram.enums import ParseMode

# Setup logger
logger = logging.getLogger(__name__)

CHUNK_SIZE = 1024 * 1024  # 1MB

async def upload_video(client: Client, message: Message, output_path, filename, duration=None, thumb=None):
    try:
        file_size = os.path.getsize(output_path)
        file_size_mb = round(file_size / (1024 * 1024), 2)
        ext = os.path.splitext(output_path)[1]
        video_duration = duration or 0

        logger.info(f"📤 Mulai upload: {filename} ({file_size_mb} MB, durasi={video_duration})")
        status_msg = await message.reply_text("📤 Menyiapkan unggahan...")

        last_update_time = 0
        start_time = time.time()

        def generate_progress_bar(current, total, length=20):
            filled = int(length * current / total)
            empty = length - filled
            return f"<code>[{'█' * filled}{'░' * empty}]</code>"

        def format_eta(seconds):
            m, s = divmod(int(seconds), 60)
            return f"{m:02}:{s:02}"

        async def progress_callback(current, total):
            nonlocal last_update_time
            now = time.time()

            if now - last_update_time < 10:
                return
            last_update_time = now

            elapsed = now - start_time
            current_mb = current / (1024 * 1024)
            speed = current_mb / elapsed if elapsed > 0 else 0
            eta = (file_size_mb - current_mb) / speed if speed > 0 else 0

            bar = generate_progress_bar(current, total)

            logger.info(f"⬆️ Upload progress: {current_mb:.2f}/{file_size_mb} MB ({speed:.2f} MB/s, ETA {format_eta(eta)})")

            text = (
                "   <b>📤 Progres Upload</b>\n\n"
                "╭━━━━━━━━━━━━━━━━━━━━━╮\n"
                f" 📝 <b>Nama:</b> <code>{filename}</code>\n"
                f" 📁 <b>Ukuran:</b> <code>{file_size_mb} MB</code>\n"
                f" 📂 <b>Ekstensi:</b> <code>{ext}</code>\n"
            )

            if video_duration:
                text += f" ⏱️ <b>Durasi:</b> <code>{video_duration} detik</code>\n"

            text += (
                f" 🚀 <b>Kecepatan:</b> <code>{speed:.2f} MB/s</code>\n"
            )

            if eta > 0:
                text += f" ⏳ <b>ETA:</b> <code>{format_eta(eta)}</code>\n"

            text += (
                f" 📦 <b>{current_mb:.2f} MB / {file_size_mb} MB</b>\n"
                f" {bar}\n"
                "╰━━━━━━━━━━━━━━━━━━━━━╯"
            )

            try:
                await status_msg.edit_text(text, parse_mode=ParseMode.HTML)
            except Exception as e:
                logger.debug(f"Gagal update status: {e}")

        await client.send_video(
            chat_id=message.chat.id,
            video=output_path,
            duration=video_duration,
            thumb=thumb,
            caption=f"✅ Selesai!\n<code>{filename}</code>",
            parse_mode=ParseMode.HTML,
            progress=progress_callback
        )

        try:
            await status_msg.delete()
        except:
            pass

        logger.info(f"✅ Upload selesai: {filename}")

        if thumb and os.path.exists(thumb):
            os.remove(thumb)
            logger.info(f"🧹 Thumbnail dihapus: {thumb}")

    except Exception as e:
        logger.exception(f"❌ Gagal mengunggah {filename}: {e}")
        await message.reply_text(f"❌ Gagal mengunggah: <code>{e}</code>", parse_mode=ParseMode.HTML)