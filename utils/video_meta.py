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
