from utils.video_meta import get_video_info  # pastikan ini sudah diimpor

async def upload_video(client, message, output_path, filename, duration=None, thumb=None):
    try:
        await client.send_video(
            chat_id=message.chat.id,
            video=output_path,
            duration=duration or None,
            thumb=thumb or None,
            caption=f"✅ Selesai!\nNama file: `{filename}`",
            parse_mode=None  # Hindari error parse_mode jika versi Pyrogram tidak mendukung
        )

        # 🧹 Hapus thumbnail jika ada
        if thumb and os.path.exists(thumb):
            os.remove(thumb)

        # 📊 Ambil dan kirim metadata video
        info = get_video_info(output_path)
        if info:
            meta_text = (
                "ℹ️ **Info Video**\n"
                f"📏 Resolusi: {info['width']}x{info['height']}\n"
                f"🎥 Durasi: {info['duration']} detik\n"
                f"🎧 Codec: {info['codec']}"
            )
            await message.reply_text(meta_text, quote=True, parse_mode=None)

    except Exception as e:
        await message.reply_text(f"❌ Gagal mengunggah: `{e}`", quote=True)
