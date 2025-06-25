import subprocess
import os
import asyncio
import sys
import time
import logging

logger = logging.getLogger(__name__)

async def download_m3u8(url: str, output_path: str, progress_callback=None) -> None:
    """
    Unduh video dari link M3U8 menggunakan ffmpeg.
    Mengirimkan progres ke output Colab dan Telegram (jika ada callback).
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

                if size_mb != last_reported_mb:
                    sys.stdout.write(f"\r📦 Terunduh: {size_mb:.2f} MB")
                    sys.stdout.flush()
                    last_reported_mb = size_mb

                now = time.time()
                if progress_callback and now - last_telegram_update >= 10:
                    await progress_callback(size_mb)
                    last_telegram_update = now

            await asyncio.sleep(0.5)

        process.wait()
        print()

        if process.returncode != 0:
            raise Exception(f"ffmpeg gagal (exit code {process.returncode})")

        if not os.path.exists(output_path):
            raise FileNotFoundError("File tidak ditemukan setelah unduhan.")

        final_size = os.path.getsize(output_path) / (1024 * 1024)
        logger.info("Download selesai: %.2f MB", final_size)

    except Exception as e:
        logger.error("Gagal mengunduh video: %s", e)
        raise Exception(f"Gagal mengunduh video: {e}")
