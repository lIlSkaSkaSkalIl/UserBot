import os
from pyrogram.enums import ParseMode  # ✅ Tambahkan ini

async def upload_video(client, message, output_path, filename, duration=None, thumb=None):
    try:
        await client.send_video(
            chat_id=message.chat.id,
            video=output_path,
            duration=duration or None,
            thumb=thumb or None,
            caption=f"✅ Selesai!\nNama file: `{filename}`",
            parse_mode=ParseMode.MARKDOWN  # ✅ Gunakan enum resmi
        )

        # 🧹 Hapus thumbnail jika ada
        if thumb and os.path.exists(thumb):
            os.remove(thumb)

    except Exception as e:
        await message.reply_text(
            f"❌ Gagal mengunggah: `{e}`",
            quote=True,
            parse_mode=ParseMode.MARKDOWN  # ✅ Tambahkan agar konsisten
        )
