import logging
from pyrogram import filters
from pyrogram.types import Message
from pyrogram.handlers import MessageHandler

# 🔧 Logger khusus untuk command handler ini
logger = logging.getLogger(__name__)

# 🔰 Fungsi yang menangani perintah /start
async def start(_, message: Message):
    user = message.from_user
    logger.info(f"👤 /start dipanggil oleh {user.first_name} (id={user.id}, username=@{user.username})")

    await message.reply_text(
        "👋 Halo!\n"
        "Kirimkan link m3u8 ke sini dan saya akan mengunduh videonya untukmu.\n\n"
        "📥 Contoh: https://example.com/video.m3u8"
    )

# 📌 Handler yang siap ditambahkan ke Pyrogram app
start_handler = MessageHandler(start, filters.command("start"))