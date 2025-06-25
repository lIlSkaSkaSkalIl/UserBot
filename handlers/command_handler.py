import logging
from pyrogram import filters
from pyrogram.types import Message
from pyrogram.handlers import MessageHandler

logger = logging.getLogger(__name__)

async def start_handler_func(_, message: Message) -> None:
    """
    Handler untuk perintah /start.
    Menjawab dengan instruksi dasar kepada pengguna.
    """
    logger.info("Menerima perintah /start dari %s", message.from_user.id)
    await message.reply_text(
        "👋 Halo!\n"
        "Kirimkan link m3u8 ke sini dan saya akan mengunduh videonya untukmu.\n\n"
        "📥 Contoh: https://example.com/video.m3u8"
    )

# Handler yang didaftarkan ke Pyrogram client
start_handler = MessageHandler(start_handler_func, filters.command("start"))
