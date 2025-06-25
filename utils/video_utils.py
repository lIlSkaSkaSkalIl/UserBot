import subprocess
import os
import asyncio
import time
import logging

logger = logging.getLogger(__name__)

async def download_m3u8(url: str, output_path: str, status_callback=None) -> None:
    """
    Unduh video dari link M3U8 menggunakan ffmpeg.
    Jika ukuran file tidak bertambah > 20 detik, hentikan update dan tunggu ffmpeg selesai.
    """
    logger.info("Memulai download dari: %s", url)

    try:
        process = subprocess.Popen(
            ["ffmpeg", "-y", "-i", url, "-c", "copy", output_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )

        last_size = -1.0
        last_size_change_time = time.time()
        status_sent = False
        progress_done = False

        while True:
            line = process.stdout.readline()
            if line == '' and process.poll() is not None:
                break

            if os.path.exists(output_path):
                size_mb = round(os.path.getsize(output_path) / (1024 * 1024), 2)
                now = time.time()

                if size_mb != last_size:
                    last_size = size_mb
                    last_size_change_time = now
                    progress_done = False

                elif not progress_done and now - last_size_change_time >= 20:
                    # Anggap download selesai, stop progress
                    msg = f"📦 Ukuran tidak berubah selama 20 detik. Download dihentikan sementara di {size_mb:.2f} MB..."
                    logger.info(msg)
                    if status_callback:
                        await status_callback(msg)
                    progress_done = True

            await asyncio.sleep(0.5)

        process.wait()

        if process.returncode != 0:
            error_msg = f"❌ ffmpeg gagal dengan kode keluar {process.returncode}"
            logger.error(error_msg)
            if status_callback:
                await status_callback(error_msg)
            raise Exception(error_msg)

        if not os.path.exists(output_path):
            raise FileNotFoundError("❌ File tidak ditemukan setelah unduhan.")

        final_size = os.path.getsize(output_path) / (1024 * 1024)
        success_msg = f"✅ Download berhasil: {final_size:.2f} MB"
        logger.info(success_msg)
        if status_callback:
            await status_callback(success_msg)

    except Exception as e:
        logger.error("Gagal mengunduh video: %s", e)
        if status_callback:
            await status_callback(f"❌ Gagal mengunduh: {e}")
        raise
