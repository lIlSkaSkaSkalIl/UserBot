import asyncio

# 🔒 Global lock untuk mencegah unduhan ganda bersamaan
global_download_lock: asyncio.Lock = asyncio.Lock()
