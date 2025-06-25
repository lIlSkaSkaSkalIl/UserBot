import subprocess
import os
import logging

logger = logging.getLogger(__name__)

def get_video_duration(path: str) -> int:
    """
    Mengambil durasi video (dalam detik) menggunakan ffprobe.
    """
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
        return int(float(result.stdout.strip()))
    except Exception as e:
        logger.error("Gagal mengambil durasi video: %s", e)
        return 0

def get_thumbnail(path: str, thumb_path: str) -> str | None:
    """
    Menghasilkan thumbnail JPG dari detik ke-1 video menggunakan ffmpeg.
    """
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
        return thumb_path if os.path.exists(thumb_path) else None
    except Exception as e:
        logger.error("Gagal mengambil thumbnail: %s", e)
        return None
