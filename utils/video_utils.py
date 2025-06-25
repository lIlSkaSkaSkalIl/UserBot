import subprocess
import os
import asyncio
import sys
import time
import logging

logger = logging.getLogger(__name__)

async def download_m3u8(url, output_path, progress_callback=None):
    """
    Unduh video M3U8 menggunakan ffmpeg.
    Menampilkan progres di Colab (MB) dan Telegram (setiap 10 detik).
    Juga mencatat semua output ffmpeg ke log.
    """
    logger.info(f"🚀 Memulai download M3U8 dari: {url}")
    print(f"[FFMPEG] 🚀 Memulai proses download dari:\n{url}\n")

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

            if line:
                logger.debug(f"[ffmpeg] {line.strip()}")  # 🔹 Log semua output ffmpeg

            # Hitung progres dari ukuran file
            if os.path.exists(output_path):
                size_mb = os.path.getsize(output_path) / (1024 * 1024)
                size_mb = round(size_mb, 2)

                # Tampilkan progres ke Colab
                if size_mb != last_reported_mb:
                    sys.stdout.write(f"\r📦 Terunduh: {size_mb:.2f} MB")
                    sys.stdout.flush()
                    last_reported_mb = size_mb
                    logger.debug(f"📦 Progres: {size_mb:.2f} MB")

                # Kirim progres ke Telegram setiap 10 detik
                now = time.time()
                if progress_callback and now - last_telegram_update >= 10:
                    await progress_callback(size_mb)
                    last_telegram_update = now

            await asyncio.sleep(0.5)

        process.wait()

        if process.returncode != 0:
            logger.error(f"❌ ffmpeg keluar dengan kode: {process.returncode}")
            raise Exception(f"ffmpeg gagal dengan kode keluar {process.returncode}")

        if not os.path.exists(output_path):
            logger.error("❌ File output tidak ditemukan setelah proses selesai.")
            raise FileNotFoundError("File tidak ditemukan setelah unduhan.")

        final_size = os.path.getsize(output_path) / (1024 * 1024)
        logger.info(f"✅ Unduhan selesai: {output_path} ({final_size:.2f} MB)")
        print()  # Baris baru untuk CLI

    except Exception as e:
        logger.exception(f"❌ Gagal mengunduh video dari {url}: {e}")
        raise Exception(f"Gagal mengunduh video: {e}")
