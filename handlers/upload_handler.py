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
        total_parts = math.ceil(file_size / CHUNK_SIZE)

        # Ambil metadata video
        info = get_video_info(output_path)
        width = info.get("width", "-")
        height = info.get("height", "-")
        codec = info.get("codec", "-")
        bitrate = info.get("bitrate", "-")
        frame_rate = info.get("frame_rate", "-")
        audio_codec = info.get("audio_codec", "-")

        # Format file size
        file_size_mb = round(file_size / (1024 * 1024), 2)

        # Caption dengan metadata
        caption = (
            "<b>✅ Upload Selesai</b>\n\n"
            f"📝 <b>Nama:</b> <code>{filename}</code>\n"
            f"🎞️ <b>Resolusi:</b> <code>{width}x{height}</code>\n"
            f"🎬 <b>Codec:</b> <code>{codec}</code>\n"
            f"🎚️ <b>Bitrate:</b> <code>{bitrate} kbps</code>\n"
            f"🎯 <b>Framerate:</b> <code>{frame_rate} fps</code>\n"
            f"🎵 <b>Audio:</b> <code>{audio_codec}</code>\n"
            f"📦 <b>Ukuran:</b> <code>{file_size_mb} MB</code>"
        )

        # Progres bar di Colab
        progress = tqdm(total=file_size, unit="B", unit_scale=True, desc="📤 Mengunggah")

        async def progress_callback(current, total):
            progress.n = current
            progress.refresh()

        await client.send_video(
            chat_id=message.chat.id,
            video=output_path,
            duration=duration or None,
            thumb=thumb or None,
            caption=caption,
            parse_mode=ParseMode.HTML,
            progress=progress_callback
        )

        progress.close()

        if thumb and os.path.exists(thumb):
            os.remove(thumb)

    except Exception as e:
        progress.close()
        await message.reply_text(f"❌ Gagal mengunggah: `{e}`")
