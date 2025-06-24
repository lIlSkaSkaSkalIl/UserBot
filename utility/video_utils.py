import subprocess
import os
import asyncio

async def download_m3u8(url, output_path, progress_callback=None):
    print(f"[FFMPEG] 🚀 Memulai proses download dari URL:\n{url}")

    try:
        process = subprocess.Popen(
            [
                "ffmpeg",
                "-y",              # overwrite file jika ada
                "-i", url,         # input URL
                "-c", "copy",      # copy stream tanpa re-encode
                output_path
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )

        # Opsional: loop jika ingin menampilkan progress
        while True:
            line = process.stdout.readline()
            if line == '' and process.poll() is not None:
                break
            await asyncio.sleep(0.5)

        process.wait()

        if process.returncode != 0:
            raise Exception(f"ffmpeg gagal dengan kode keluar {process.returncode}")

        if not os.path.exists(output_path):
            raise FileNotFoundError("❌ File tidak ditemukan setelah unduhan.")

        size = os.path.getsize(output_path)
        if size < 1024:
            raise Exception("❌ Ukuran file terlalu kecil, kemungkinan gagal.")

        print(f"[FFMPEG] ✅ Unduhan selesai: {output_path} ({size / 1024:.2f} KB)")

    except Exception as e:
        print(f"[FFMPEG] ❌ Terjadi kesalahan: {e}")
        raise
