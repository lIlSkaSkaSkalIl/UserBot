import os
import math
from tqdm import tqdm
from pyrogram.types import Message
from pyrogram import Client

CHUNK_SIZE = 1024 * 1024  # 1MB

async def upload_video(client: Client, message: Message, output_path, filename, duration=None, thumb=None):
    try:
        file_size = os.path.getsize(output_path)
        total_parts = math.ceil(file_size / CHUNK_SIZE)

        # Progress bar
        progress = tqdm(total=file_size, unit="B", unit_scale=True, desc="📤 Mengunggah")

        async def progress_callback(current, total):
            progress.n = current
            progress.refresh()

        await client.send_video(
            chat_id=message.chat.id,
            video=output_path,
            duration=duration or None,
            thumb=thumb or None,
            caption=f"✅ Selesai!\nNama file: `{filename}`",
            progress=progress_callback
        )

        progress.close()

        if thumb and os.path.exists(thumb):
            os.remove(thumb)

    except Exception as e:
        progress.close()
        await message.reply_text(f"❌ Gagal mengunggah: `{e}`")
