import subprocess
import os
import json

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
        return int(float(result.stdout.strip()))
    except Exception as e:
        print(f"❌ Gagal mengambil durasi: {e}")
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
        return thumb_path if os.path.exists(thumb_path) else None
    except Exception as e:
        print(f"❌ Gagal mengambil thumbnail: {e}")
        return None

def get_video_info(path: str) -> dict:
    """Mengambil metadata lengkap video."""
    try:
        if not os.path.exists(path):
            raise FileNotFoundError("File video tidak ditemukan")

        result = subprocess.run(
            [
                "ffprobe", "-v", "error",
                "-select_streams", "v:0,a:0",
                "-show_entries",
                "format=duration,bit_rate:stream=index,codec_type,codec_name,width,height,r_frame_rate,sample_rate",
                "-of", "json",
                path
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # ✅ Cetak output mentah JSON dari ffprobe untuk debugging di Colab
        print("\n===== [FFPROBE RAW JSON OUTPUT] =====")
        print(result.stdout)
        print("=====================================\n")

        if not result.stdout:
            raise ValueError("Output ffprobe kosong")

        data = json.loads(result.stdout)

        streams = data.get("streams", [])
        if not streams:
            raise ValueError("Tidak ada stream ditemukan dalam metadata")

        video_stream = next((s for s in streams if s.get("codec_type") == "video"), {})
        audio_stream = next((s for s in streams if s.get("codec_type") == "audio"), {})
        format_info = data.get("format", {})

        return {
            "duration": int(float(format_info.get("duration", 0))),
            "bitrate": int(format_info.get("bit_rate", 0)) // 1000 if format_info.get("bit_rate") else None,
            "width": video_stream.get("width"),
            "height": video_stream.get("height"),
            "codec": video_stream.get("codec_name"),
            "frame_rate": eval(video_stream.get("r_frame_rate", "0")) if "r_frame_rate" in video_stream else None,
            "audio_codec": audio_stream.get("codec_name"),
            "sample_rate": int(audio_stream.get("sample_rate", 0)) if "sample_rate" in audio_stream else None,
        }

    except Exception as e:
        print(f"❌ Gagal mengambil info video: {e}")
        return {}
