import os

async def upload_video(client, message, output_path, filename, duration=None, thumb=None):
    try:
        await client.send_video(
            chat_id=message.chat.id,
            video=output_path,
            duration=duration or None,
            thumb=thumb or None,
            caption=f"✅ Selesai!\nNama file: `{filename}`",
            parse_mode="Markdown"
        )

        # 🧹 Hapus thumbnail jika ada
        if thumb and os.path.exists(thumb):
            os.remove(thumb)

    except Exception as e:
        await message.reply_text(f"❌ Gagal mengunggah: `{e}`", quote=True)
