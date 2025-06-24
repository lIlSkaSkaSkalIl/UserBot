import os
import math
from tqdm import tqdm
from pyrogram.types import Message
from pyrogram import Client
from pyrogram.enums import ParseMode

from utils.video_meta import get_video_info

CHUNK_SIZE = 1024 * 1024  # 1MB

async def upload_video(client: Client, message: Message, output_path, filename, duration=None, thumb=None):
    try:
        file_size = os.path.getsize(output_path)
        file_size_mb = round(file_size / (1024 * 1024), 2)
        ext = os.path.splitext(output_path)[1]

        # Ambil metadata jika tersedia
        info = get_video_info(output_path)
        width = info.get("width")
        height = info.get("height")
        video_duration = info.get("duration", duration)

        # Siapkan status message awal
        status_msg = await message.reply_text("📤 Menyiapkan unggahan...")

        # Inisialisasi progress bar
        progress = tqdm(total=file_size, unit="B", unit_scale=True, desc="📤 Mengunggah")

        def generate_progress_bar(current, total, length=20):
            filled = int(length * current / total)
            empty = length - filled
            return f"<code>[{'█' * filled}{'░' * empty}]</code>"

        async def progress_callback(current, total):
            current_mb = current / (1024 * 1024)
            bar = generate_progress_bar(current, total)

            text = (
                "<b>📤 Progres Upload</b>\n"
                "╭━━━━━━━━━━━━━━━━━━━━━╮\n"
                f"📝 <b>Nama:</b> <code>{filename}</code>\n"
                f"📁 <b>Ukuran:</b> <code>{file_size_mb} MB</code>\n"
                f"📂 <b>Ekstensi:</b> <code>{ext}</code>\n"
            )

            if video_duration:
                text += f"⏱️ <b>Durasi:</b> <code>{video_duration} detik</code>\n"
            if width and height:
                text += f"📏 <b>Resolusi:</b> <code>{width}x{height}</code>\n"

            text += (
                f"{bar}\n"
                f"📦 <b>{current_mb:.2f} MB / {file_size_mb} MB</b>\n"
                "╰━━━━━━━━━━━━━━━━━━━━━╯"
            )

            try:
                await status_msg.edit_text(text, parse_mode=ParseMode.HTML)
            except:
                pass

            progress.n = current
            progress.refresh()

        # Kirim file
        await client.send_video(
            chat_id=message.chat.id,
            video=output_path,
            duration=video_duration or None,
            thumb=thumb or None,
            caption=f"✅ Selesai!\n<code>{filename}</code>",
            parse_mode=ParseMode.HTML,
            progress=progress_callback
        )

        progress.close()

        if thumb and os.path.exists(thumb):
            os.remove(thumb)

    except Exception as e:
        progress.close()
        await message.reply_text(f"❌ Gagal mengunggah: <code>{e}</code>", parse_mode=ParseMode.HTML)
