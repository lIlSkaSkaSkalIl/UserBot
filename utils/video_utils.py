import subprocess
import os
import asyncio
import time
import logging

logger = logging.getLogger(__name__)

async def download_m3u8(url: str, output_path: str, progress_callback=None, status_callback=None):
    """
    Mengunduh video M3U8 menggunakan ffmpeg, dengan opsi untuk update progres dan status.
    """
    logger.info("Memulai download dari: %s", url)
    if status_callback:
        await status_callback("📥 Memulai download dari FFmpeg...")

    try:
        process = subprocess.Popen(
            ["ffmpeg", "-y", "-i", url, "-c", "copy", output_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )

        last_size = -1
        last_update_time = time.time()
        stalled_time = 0

        while True:
            if os.path.exists(output_path):
                size = os.path.getsize(output_path)
                size_mb = round(size / (1024 * 1024), 2)

                if size != last_size:
                    stalled_time = 0
                    last_size = size
                    if progress_callback:
                        await progress_callback(size_mb)
                else:
                    stalled_time += 0.5
                    if stalled_time > 20 and status_callback:
                        await status_callback("⚠️ FFmpeg lambat atau macet, menunggu proses...")

                await asyncio.sleep(0.5)

            if process.poll() is not None:
                break

        if status_callback:
            await status_callback("✅ FFmpeg selesai. Menyelesaikan proses...")

        if process.returncode != 0:
            raise Exception(f"ffmpeg gagal dengan kode keluar {process.returncode}")

        if not os.path.exists(output_path):
            raise FileNotFoundError("File hasil unduhan tidak ditemukan.")

        final_size = os.path.getsize(output_path) / (1024 * 1024)
        logger.info("Download selesai: %.2f MB", final_size)
        if status_callback:
            await status_callback(f"✅ Validasi selesai. Ukuran akhir: {final_size:.2f} MB")

    except Exception as e:
        logger.error("Gagal mengunduh video: %s", e)
        if status_callback:
            await status_callback(f"❌ Gagal mengunduh: {e}")
        raise
