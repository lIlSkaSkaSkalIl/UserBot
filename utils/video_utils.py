import subprocess
import os
import asyncio
import time
import logging

logger = logging.getLogger(__name__)

async def download_m3u8(url: str, output_path: str, progress_callback=None) -> None:
    """
    Unduh video dari link M3U8 menggunakan ffmpeg.
    Hanya mengirimkan progres ke Telegram (jika disediakan).
    Tidak menampilkan progres di terminal.
    Tidak melakukan validasi file setelah unduhan selesai.
    """
    logger.info("Memulai download dari: %s", url)

    try:
        process = subprocess.Popen(
            ["ffmpeg", "-y", "-i", url, "-c", "copy", output_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )

        last_reported_mb = -1.0
        last_telegram_update = 0

        while True:
            line = process.stdout.readline()
            if line == '' and process.poll() is not None:
                break

            if os.path.exists(output_path):
                size_mb = os.path.getsize(output_path) / (1024 * 1024)
                size_mb = round(size_mb, 2)

                # Hanya kirim ke Telegram jika ukuran berubah dan waktu update cukup lama
                now = time.time()
                if (
                    progress_callback and 
                    size_mb != last_reported_mb and 
                    now - last_telegram_update >= 10
                ):
                    await progress_callback(size_mb)
                    last_telegram_update = now
                    last_reported_mb = size_mb

            await asyncio.sleep(0.5)

        process.wait()

        if process.returncode != 0:
            raise Exception(f"ffmpeg gagal (exit code {process.returncode})")

        logger.info("🎉 Unduhan selesai oleh ffmpeg: %s", output_path)

    except Exception as e:
        logger.error("Gagal mengunduh video: %s", e)
        raise Exception(f"Gagal mengunduh video: {e}")
