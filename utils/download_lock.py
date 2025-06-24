import asyncio

# Global lock untuk membatasi hanya satu unduhan aktif dalam satu waktu
global_download_lock = asyncio.Lock()
