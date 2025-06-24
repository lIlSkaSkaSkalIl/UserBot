import subprocess
import os
import asyncio
import sys

async def download_m3u8(url, output_path):
    print(f"[FFMPEG] 🚀 Memulai proses download dari:\n{url}")

    try:
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

        last_reported = -1  # Hindari print berulang
        while True:
            line = process.stdout.readline()
            if line == '' and process.poll() is not None:
                break

            if os.path.exists(output_path):
                size_mb = os.path.getsize(output_path) / (1024 * 1024)
                size_mb = round(size_mb, 2)
                if size_mb != last_reported:
                    print(f"📦 Terunduh: {size_mb} MB", end="\r")
                    sys.stdout.flush()
                    last_reported = size_mb

            await asyncio.sleep(1)

        process.wait()
        print()  # Pindah baris setelah progress

        if process.returncode != 0:
            raise Exception(f"ffmpeg gagal dengan kode keluar {process.returncode}")

        if not os.path.exists(output_path):
            raise FileNotFoundError("File tidak ditemukan setelah unduhan.")

        final_size = os.path.getsize(output_path) / (1024 * 1024)
        print(f"✅ Unduhan selesai. Total: {final_size:.2f} MB")

    except Exception as e:
        raise Exception(f"Gagal mengunduh video: {e}")
