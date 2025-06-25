import subprocess  # Untuk menjalankan proses eksternal (ffmpeg)
import os          # Untuk operasi file dan path
import asyncio     # Untuk async sleep dan event loop
import sys         # Untuk menulis ke output terminal
import time        # Untuk menghitung durasi dan ETA
import logging     # Untuk mencatat log ke file atau terminal

logger = logging.getLogger(__name__)

async def download_m3u8(url: str, output_path: str, progress_callback=None) -> None:
    """
    Mengunduh video dari link M3U8 menggunakan `ffmpeg`.

    Params:
    - url (str): Link M3U8 yang ingin diunduh.
    - output_path (str): Lokasi file output hasil unduhan.
    - progress_callback (Callable): Fungsi async opsional untuk mengirimkan progres ke Telegram.

    Progres ditampilkan di output terminal (Colab) dan Telegram jika `progress_callback` diberikan.
    """
    logger.info("Memulai download dari: %s", url)

    try:
        # Jalankan ffmpeg sebagai proses eksternal untuk mengunduh video
        process = subprocess.Popen(
            ["ffmpeg", "-y", "-i", url, "-c", "copy", output_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )

        # Inisialisasi variabel pelacakan progres
        last_reported_mb = -1.0
        last_telegram_update = 0

        # Baca output dari ffmpeg secara terus-menerus
        while True:
            line = process.stdout.readline()
            if line == '' and process.poll() is not None:
                break  # Keluar jika proses selesai

            # Jika file output sudah terbentuk, ukur ukuran file-nya
            if os.path.exists(output_path):
                size_mb = os.path.getsize(output_path) / (1024 * 1024)
                size_mb = round(size_mb, 2)

                # Tampilkan progres di output terminal (Colab)
                if size_mb != last_reported_mb:
                    sys.stdout.write(f"\r📦 Terunduh: {size_mb:.2f} MB")
                    sys.stdout.flush()
                    last_reported_mb = size_mb

                # Kirim update progres ke Telegram setiap 10 detik
                now = time.time()
                if progress_callback and now - last_telegram_update >= 10:
                    await progress_callback(size_mb)
                    last_telegram_update = now

            await asyncio.sleep(0.5)

        # Tunggu hingga proses ffmpeg benar-benar selesai
        process.wait()
        print("🎉 Download dari ffmpeg selesai.")
        logger.info("🎉 ffmpeg selesai mengunduh.")

        # Validasi apakah file benar-benar terunduh dan tidak rusak
        print("🔎 Memvalidasi file hasil download...")
        logger.info("🔎 Memvalidasi file hasil download...")

        if process.returncode != 0:
            raise Exception(f"ffmpeg gagal (exit code {process.returncode})")

        if not os.path.exists(output_path):
            raise FileNotFoundError("File tidak ditemukan setelah unduhan.")

        # Log informasi ukuran file akhir
        final_size = os.path.getsize(output_path) / (1024 * 1024)
        logger.info("Download selesai: %.2f MB", final_size)
        logger.info("✅ Validasi berhasil. File siap diproses.")
        print("✅ Validasi berhasil. File siap diproses.")

    except Exception as e:
        # Tangani dan log error jika terjadi kesalahan
        logger.error("Gagal mengunduh video: %s", e)
        raise Exception(f"Gagal mengunduh video: {e}")
