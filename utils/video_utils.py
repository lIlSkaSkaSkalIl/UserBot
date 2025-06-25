import subprocess
import os
import asyncio
import sys
import time
import logging

logger = logging.getLogger(__name__)

async def download_m3u8(url, output_path, progress_callback=None):
    """
    Unduh video M3U8 menggunakan N_m3u8DL-RE (lebih cepat dari ffmpeg).
    Menampilkan progres (MB) ke CLI dan Telegram setiap 10 detik.
    """
    binary_path = "./bin/N_m3u8DL-RE"
    logger.info(f"🚀 Memulai download M3U8 dari: {url}")
    print(f"[M3U8DL] 🚀 Proses download:\n{url}\n")

    try:
        # Pastikan tool bisa dieksekusi
        if not os.access(binary_path, os.X_OK):
            subprocess.run(["chmod", "+x", binary_path])
            logger.info("🔐 Permission +x diberikan ke N_m3u8DL-RE")

        # Setup nama file dan path
        save_dir = os.path.dirname(output_path)
        base_name = os.path.splitext(os.path.basename(output_path))[0]
        final_path = os.path.join(save_dir, f"{base_name}.mkv")  # Karena --format=mkv

        cmd = [
            binary_path,
            "-M", "format=mkv",
            "--save-name", base_name,
            "--save-dir", save_dir,
            url
        ]
        logger.debug(f"📥 Menjalankan command: {' '.join(cmd)}")

        process = subprocess.Popen(
            cmd,
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
                logger.debug(f"[M3U8DL] {line.strip()}")

            if os.path.exists(final_path):
                size_mb = round(os.path.getsize(final_path) / (1024 * 1024), 2)

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

        if process.returncode != 0:
            logger.error(f"❌ N_m3u8DL-RE keluar dengan kode: {process.returncode}")
            raise Exception(f"N_m3u8DL-RE gagal (code {process.returncode})")

        if not os.path.exists(final_path):
            raise FileNotFoundError("❌ File output tidak ditemukan setelah unduhan.")

        final_size = os.path.getsize(final_path) / (1024 * 1024)
        logger.info(f"✅ Unduhan selesai: {final_path} ({final_size:.2f} MB)")
        print()

        # Rename agar sesuai dengan output_path (mp4)
        if final_path != output_path:
            os.rename(final_path, output_path)
            logger.info(f"🔁 File diubah dari {final_path} ➜ {output_path}")

    except Exception as e:
        logger.exception(f"❌ Gagal mengunduh video dari {url}: {e}")
        raise Exception(f"Gagal mengunduh video: {e}")
