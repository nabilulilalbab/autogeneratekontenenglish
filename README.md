

```markdown
# Language Learning Video Generator

Proyek ini dirancang untuk membuat video pembelajaran bahasa yang mencakup kalimat-kalimat dalam bahasa Inggris beserta terjemahannya ke dalam bahasa Indonesia. Video ini juga dilengkapi penjelasan untuk setiap kata dalam kalimat yang diajarkan.  

## Fitur
- Pembuatan video pembelajaran otomatis.
- Text-to-Speech (TTS) menggunakan `gTTS`.
- Efek visual dengan teks terjemahan dan penjelasan kata.
- Kemampuan untuk menggunakan gambar latar kustom.

## Persyaratan
Pastikan Anda memiliki semua dependensi yang diperlukan. Anda dapat menginstalnya menggunakan perintah berikut:  

```

```bash
pip install -r requirements.txt
```

### Dependencies
- `gTTS`: Untuk mengonversi teks menjadi suara.
- `moviepy`: Untuk membuat dan mengedit video.
- `Pillow`: Untuk manipulasi gambar.
- `ImageMagick`: Digunakan oleh MoviePy untuk memproses teks.

## Struktur Proyek
```
Belajar/
└── char/
    └── automationbeginner/
        └── fix/
            ├── main.py
            ├── requirements.txt
            └── background.jpeg
```

## Cara Menggunakan
1. Tambahkan kalimat yang ingin Anda pelajari di variabel `SENTENCES` dalam file `main.py`. Struktur setiap kalimat:  
    ```python
    {
        "en": "How are you?",  # Kalimat dalam Bahasa Inggris
        "id": "Apa kabar?",    # Terjemahan dalam Bahasa Indonesia
        "explanation": {       # Penjelasan kata per kata
            "How": "Bagaimana",
            "Are": "Adalah",
            "You": "Kamu"
        }
    }
    ```
2. Jalankan file Python untuk menghasilkan video:  
    ```bash
    python main.py
    ```
3. Video akan disimpan dalam file `output_video.mp4`.

## Catatan Penting
- Pastikan `ImageMagick` telah diinstal di sistem Anda. Jika belum, Anda dapat menginstalnya dengan:
  - Ubuntu/Debian:  
    ```bash
    sudo apt install imagemagick
    ```
  - Arch Linux:  
    ```bash
    sudo pacman -S imagemagick
    ```
- Konfigurasikan lokasi `IMAGEMAGICK_BINARY` di `main.py` jika diperlukan. Default:  
  ```python
  change_settings({"IMAGEMAGICK_BINARY": "/usr/bin/magick"})
  ```

## Lisensi
Proyek ini menggunakan lisensi **MIT**. Silakan gunakan dan modifikasi sesuai kebutuhan Anda.

## Kontak
Jika Anda memiliki pertanyaan atau masalah, silakan hubungi kami di:  
📧 Email: [nabilulilalbab@gmail.com]  
🌐 Website: [https://portfolio.nabiel.biz.id]  

---

Selamat belajar bahasa Inggris dan semoga sukses!
```
