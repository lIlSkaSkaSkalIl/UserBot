from pyrogram import filters
from pyrogram.types import Message
from pyrogram.handlers import MessageHandler

# 🔰 Fungsi yang menangani perintah /start
async def start(_, message: Message):
    await message.reply_text(
        "👋 Halo!\n"
        "Kirimkan link m3u8 ke sini dan saya akan mengunduh videonya untukmu.\n\n"
        "📥 Contoh: https://example.com/video.m3u8"
    )

# 📌 Handler yang siap ditambahkan ke Pyrogram app
start_handler = MessageHandler(start, filters.command("start"))
