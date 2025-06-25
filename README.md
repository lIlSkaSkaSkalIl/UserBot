
# M3U8 Downloader Telegram UserBot

M3U8 Downloader Telegram UserBot adalah bot otomatis berbasis [Pyrogram v2.0.106](https://docs.pyrogram.org/) yang dapat mengunduh video dari link M3U8 dan mengunggahnya langsung ke Telegram melalui akun pribadi (userbot).

> 📌 Versi: v1 (Stabil)

---

## 📚 Fitur Utama

- 🔗 Mendukung unduhan video dari file `.m3u8`
- 📤 Upload otomatis ke Telegram setelah selesai download
- 🎯 Built-in command handler dan status monitor
- 💡 Lock system untuk mencegah bentrok download ganda
- 📁 Terstruktur modular: mudah untuk di-maintain dan dikembangkan
- ⚙️ Gunakan `session string` untuk login userbot

---

## 🚀 Jalankan di Google Colab

Klik tombol berikut untuk menjalankan langsung di Google Colab:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lIlSkaSkaSkalIl/UserBot/blob/main/m3u8doenloaderUserBotWstatus-stable/M3U8%20Telegram%20userbot.ipynb)

---

## 🛠️ Cara Menggunakan (Colab)

1. Buka notebook [M3U8 Telegram userbot.ipynb](https://github.com/lIlSkaSkaSkalIl/UserBot/blob/main/m3u8doenloaderUserBotWstatus-stable/M3U8%20Telegram%20userbot.ipynb)
2. Jalankan sel satu per satu
3. Masukkan `PYROGRAM_SESSION_STRING` saat diminta
4. Kirimkan perintah melalui Telegram ke akun userbot Anda:
   - `/download <link.m3u8>`
   - Bot akan mengunduh video dan mengunggahnya kembali ke Telegram

---

## 📦 Struktur Proyek

```
m3u8doenloaderUserBotWstatus-stable/
├── main.py                      # Main entry point
├── requirements.txt             # Dependencies
├── handlers/                    # Command, download, upload logic
├── utility/                     # Video processing helpers
├── utils/                       # Locking & metadata
└── M3U8 Telegram userbot.ipynb  # Colab notebook
```

---

## 🔧 Instalasi Manual (Opsional)

Untuk developer lanjutan:
```bash
git clone https://github.com/lIlSkaSkaSkalIl/UserBot.git
cd UserBot/m3u8doenloaderUserBotWstatus-stable
pip install -r requirements.txt
python main.py
```

---

## 📄 Lisensi

MIT License - bebas digunakan dan dimodifikasi.

---

## ✨ Credits

Dikembangkan oleh [@lIlSkaSkaSkalIl](https://github.com/lIlSkaSkaSkalIl).  
Gunakan dengan bijak.
