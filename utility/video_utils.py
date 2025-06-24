import subprocess
import os
import asyncio
from tqdm import tqdm

async def download_m3u8(url: str, output_path: str):
    """
    Unduh video dari M3U8 menggunakan ffmpeg dan tampilkan progress bar di Colab/terminal.
    """
    print(f"[FFMPEG] 🚀 Memulai unduhan:\n{url}")
    print(f"[FFMPEG] 📦 Menyimpan ke: {output_path}")

    try:
        # Estimasi durasi total (opsional, tergantung m3u8 info)
        total_duration = 60 * 10  # Misal 10 menit (600 detik)
        progress = tqdm(total=total_duration, desc="📥 Mengunduh", unit="detik")

        process = subprocess.Popen(
            [
                "ffmpeg",
                "-y",
                "-i", url,
                "-c", "copy",
                output_path
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )

        while True:
            line = process.stdout.readline()
            if line == '' and process.poll() is not None:
                break

            if "time=" in line:
                try:
                    # Ekstrak durasi saat ini dari output ffmpeg
                    time_str = line.split("time=")[-1].split(" ")[0].strip()
                    h, m, s = map(float, time_str.split(":"))
                    current_sec = int(h * 3600 + m * 60 + s)
                    progress.n = current_sec
                    progress.refresh()
                except Exception:
                    pass

            await asyncio.sleep(0.2)

        process.wait()
        progress.close()

        if process.returncode != 0:
            raise Exception(f"ffmpeg gagal dengan kode keluar {process.returncode}")

        if not os.path.exists(output_path):
            raise FileNotFoundError("❌ File tidak ditemukan setelah proses unduh.")

        size = os.path.getsize(output_path)
        if size < 1024:
            raise Exception("❌ File terlalu kecil, kemungkinan gagal.")

        print(f"✅ Unduhan selesai ({round(size / (1024 * 1024), 2)} MB)")

    except Exception as e:
        print(f"❌ Gagal mengunduh: {e}")
        raise
