import subprocess
import os
import logging

# Setup logger
logger = logging.getLogger(__name__)

def get_video_duration(path: str) -> int:
    """Mengambil durasi video (dalam detik) menggunakan ffprobe."""
    try:
        result = subprocess.run(
            [
                "ffprobe", "-v", "error",
                "-select_streams", "v:0",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                path
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        duration_str = result.stdout.strip()
        duration = int(float(duration_str))
        logger.info(f"📏 Durasi video: {duration} detik — {path}")
        return duration
    except Exception as e:
        logger.warning(f"❌ Gagal mengambil durasi video ({path}): {e}")
        return 0

def get_thumbnail(path: str, thumb_path: str) -> str:
    """Menghasilkan thumbnail JPG dari detik ke-1 video."""
    try:
        subprocess.run(
            [
                "ffmpeg", "-y", "-i", path,
                "-ss", "00:00:01.000", "-vframes", "1",
                "-s", "480x270",
                thumb_path
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        if os.path.exists(thumb_path):
            logger.info(f"🖼️ Thumbnail berhasil dibuat: {thumb_path}")
            return thumb_path
        else:
            logger.warning(f"❌ Thumbnail gagal dibuat (file tidak ditemukan): {thumb_path}")
            return None
    except Exception as e:
        logger.error(f"❌ Gagal membuat thumbnail dari {path}: {e}")
        return None