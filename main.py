from gtts import gTTS
from moviepy.editor import TextClip, CompositeVideoClip, ImageClip, AudioFileClip, concatenate_videoclips, concatenate_audioclips, vfx
from moviepy.config import change_settings
from moviepy.video.fx.all import speedx
from PIL import Image
import os



key = "q3c5bAJCSDLrS1zehfInYOfckKNcdi8KjXWf0awgxrXpGy7sEBrxBtL4"


# Mengubah konfigurasi MoviePy untuk menggunakan `magick`
change_settings({"IMAGEMAGICK_BINARY": "/usr/bin/magick"})

def generate_language_learning_video(
    sentences,
    default_background_path="background.jpeg",
    output_file="output_video.mp4"
):
    video_components = []
    audio_files = set()

    def create_text_clip(text, fontsize, duration, position='center'):
        try:
            clip = TextClip(text, fontsize=fontsize, color='white',
                            font='amiri/Amiri-Regular.ttf', bg_color='black', method='caption',
                            size=(1920, 200))
            clip = clip.set_position(position).set_duration(duration)
            return clip
        except Exception:
            clip = TextClip(text, fontsize=fontsize, color='white',
                            bg_color='black', method='caption',
                            size=(1920, 200))
            clip = clip.set_position(position).set_duration(duration)
            return clip

    for sentence in sentences:
        # Pilih background
        background_path = sentence.get('background', default_background_path)

        # Cek apakah file background ada
        if not os.path.exists(background_path):
            print(f"Warning: Background {background_path} not found. Using default.")
            background_path = default_background_path

        background = Image.open(background_path).resize((1920, 1080), Image.LANCZOS)
        background.save(f"background_{sentences.index(sentence)}.jpeg")
        background_clip = ImageClip(f"background_{sentences.index(sentence)}.jpeg")

        # Text-to-Speech
        en_tts = gTTS(text=sentence['en'], lang='en')
        id_tts = gTTS(text=sentence['id'], lang='id')

        en_audio_file = f"en_sentence_{sentences.index(sentence)}.mp3"
        id_audio_file = f"id_sentence_{sentences.index(sentence)}.mp3"

        en_tts.save(en_audio_file)
        id_tts.save(id_audio_file)

        audio_files.update([en_audio_file, id_audio_file])

        # Klip kalimat Inggris (dengan slow motion jika ditentukan)
        slowmo = sentence.get('slowmo', 1.0)
        en_text_clip = create_text_clip(sentence['en'], fontsize=60, duration=5)
        en_audio_clip = AudioFileClip(en_audio_file)

        en_video_clip = CompositeVideoClip([
            background_clip.set_duration(5),
            en_text_clip
        ], size=(1920, 1080))

        # Terapkan slow motion jika ada
        if slowmo != 1.0:
            en_audio_clip = en_audio_clip.fx(vfx.speedx, slowmo)
            en_video_clip = en_video_clip.fx(vfx.speedx, slowmo)

        en_video_clip = en_video_clip.set_audio(en_audio_clip)
        video_components.append(en_video_clip)

        # Klip kalimat Indonesia
        id_text_clip = create_text_clip(sentence['id'], fontsize=60, duration=5)
        id_audio_clip = AudioFileClip(id_audio_file)
        id_video_clip = CompositeVideoClip([
            background_clip.set_duration(5),
            id_text_clip
        ], size=(1920, 1080))
        id_video_clip = id_video_clip.set_audio(id_audio_clip)
        video_components.append(id_video_clip)

        # Klip penjelasan kata
        for word, meaning in sentence['explanation'].items():
            word_en_tts = gTTS(text=word, lang='en')
            word_id_tts = gTTS(text=meaning, lang='id')

            word_en_audio = f"{word}_en.mp3"
            word_id_audio = f"{word}_id.mp3"

            word_en_tts.save(word_en_audio)
            word_id_tts.save(word_id_audio)

            audio_files.update([word_en_audio, word_id_audio])

            # Klip teks dan audio untuk kata
            word_en_clip = create_text_clip(word, fontsize=50, duration=2)
            word_id_clip = create_text_clip(meaning, fontsize=50, duration=3)

            word_en_audio_clip = AudioFileClip(word_en_audio)
            word_id_audio_clip = AudioFileClip(word_id_audio)

            combined_audio = concatenate_audioclips([word_en_audio_clip, word_id_audio_clip])

            word_video_clip = CompositeVideoClip([
                background_clip.set_duration(5),
                word_en_clip.set_start(0),
                word_id_clip.set_start(2)
            ], size=(1920, 1080))

            word_video_clip = word_video_clip.set_audio(combined_audio)
            video_components.append(word_video_clip)

        # Klip kalimat Inggris di akhir
        en_text_clip_end = create_text_clip(sentence['en'], fontsize=60, duration=5)
        en_audio_clip_end = AudioFileClip(en_audio_file)

        en_video_clip_end = CompositeVideoClip([
            background_clip.set_duration(5),
            en_text_clip_end
        ], size=(1920, 1080))

        # Terapkan slow motion jika ada
        if slowmo != 1.0:
            en_audio_clip_end = en_audio_clip_end.fx(vfx.speedx, slowmo)
            en_video_clip_end = en_video_clip_end.fx(vfx.speedx, slowmo)

        en_video_clip_end = en_video_clip_end.set_audio(en_audio_clip_end)
        video_components.append(en_video_clip_end)

    # Gabungkan video
    final_video = concatenate_videoclips(video_components)
    final_video.write_videofile(output_file, codec='libx264', fps=24)

    # Bersihkan file sementara
    cleanup_files = [
        f"background_{i}.jpeg" for i in range(len(sentences))
    ] + list(audio_files)

    for file in cleanup_files:
        if os.path.exists(file):
            os.remove(file)

    return output_file

# Contoh penggunaan lengkap
SENTENCES = [

        {
            "en": "How are you?",
            "id": "Apa kabar?",
            "explanation": {
                "How": "Bagaimana",
                "Are": "Adalah (kata kerja bentuk to be untuk 'kamu')",
                "You": "Kamu"
            }
        },
        {
            "en": "What is your name?",
            "id": "Siapa namamu?",
            "explanation": {
                "What": "Apa",
                "Is": "Adalah",
                "Your": "Kamu (kepemilikan)",
                "Name": "Nama"
            }
        },
        {
            "en": "Where are you from?",
            "id": "Dari mana asalmu?",
            "explanation": {
                "Where": "Di mana",
                "Are": "Adalah (kata kerja bentuk to be untuk 'kamu')",
                "You": "Kamu",
                "From": "Dari"
            }
        },
        {
            "en": "I am fine, thank you.",
            "id": "Saya baik-baik saja, terima kasih.",
            "explanation": {
                "I": "Saya",
                "Am": "Adalah (kata kerja bentuk to be untuk 'saya')",
                "Fine": "Baik-baik saja",
                "Thank": "Terima kasih",
                "You": "Kamu"
            }
        },
        {
            "en": "Nice to meet you.",
            "id": "Senang bertemu denganmu.",
            "explanation": {
                "Nice": "Senang",
                "To": "Untuk",
                "Meet": "Bertemu",
                "You": "Kamu"
            }
        },
        {
            "en": "What time is it?",
            "id": "Jam berapa sekarang?",
            "explanation": {
                "What": "Apa",
                "Time": "Waktu",
                "Is": "Adalah",
                "It": "Ini"
            }
        },
        {
            "en": "How much is this?",
            "id": "Berapa harganya?",
            "explanation": {
                "How": "Berapa",
                "Much": "Banyak",
                "Is": "Adalah",
                "This": "Ini"
            }
        },
        {
            "en": "Where is the restroom?",
            "id": "Di mana kamar kecil?",
            "explanation": {
                "Where": "Di mana",
                "Is": "Adalah",
                "The": "(Kata sandang)",
                "Restroom": "Kamar kecil"
            }
        },
        {
            "en": "Can you help me?",
            "id": "Bisakah kamu membantu saya?",
            "explanation": {
                "Can": "Bisa",
                "You": "Kamu",
                "Help": "Membantu",
                "Me": "Saya"
            }
        },
        {
            "en": "I don't understand.",
            "id": "Saya tidak mengerti.",
            "explanation": {
                "I": "Saya",
                "Don't": "Tidak (do not)",
                "Understand": "Mengerti"
            }
        },
        {
            "en": "Could you repeat that?",
            "id": "Bisakah kamu mengulanginya?",
            "explanation": {
                "Could": "Bisakah",
                "You": "Kamu",
                "Repeat": "Mengulangi",
                "That": "Itu"
            }
        },
        {
            "en": "Excuse me, where is the bus station?",
            "id": "Permisi, di mana stasiun bus?",
            "explanation": {
                "Excuse": "Permisi",
                "Me": "Saya",
                "Where": "Di mana",
                "Is": "Adalah",
                "The": "(Kata sandang)",
                "Bus": "Bus",
                "Station": "Stasiun"
            }
        },
        {
            "en": "I'm sorry, I don't know.",
            "id": "Maaf, saya tidak tahu.",
            "explanation": {
                "I'm": "Saya adalah (I am)",
                "Sorry": "Maaf",
                "I": "Saya",
                "Don't": "Tidak (do not)",
                "Know": "Tahu"
            }
        },
        {
            "en": "Can you speak English?",
            "id": "Bisakah kamu berbicara bahasa Inggris?",
            "explanation": {
                "Can": "Bisa",
                "You": "Kamu",
                "Speak": "Berbicara",
                "English": "Bahasa Inggris"
            }
        },
        {
            "en": "What does this mean?",
            "id": "Apa arti ini?",
            "explanation": {
                "What": "Apa",
                "Does": "Apakah",
                "This": "Ini",
                "Mean": "Berarti"
            }
        },
        {
            "en": "Can you show me the way?",
            "id": "Bisakah kamu menunjukkan jalan?",
            "explanation": {
                "Can": "Bisa",
                "You": "Kamu",
                "Show": "Menunjukkan",
                "Me": "Saya",
                "The": "(Kata sandang)",
                "Way": "Jalan"
            }
        },
        {
            "en": "I would like to order this.",
            "id": "Saya ingin memesan ini.",
            "explanation": {
                "I": "Saya",
                "Would": "Akan",
                "Like": "Ingin",
                "To": "Untuk",
                "Order": "Memesan",
                "This": "Ini"
            }
        },
        {
            "en": "How do you say this in English?",
            "id": "Bagaimana kamu mengucapkan ini dalam bahasa Inggris?",
            "explanation": {
                "How": "Bagaimana",
                "Do": "Apakah",
                "You": "Kamu",
                "Say": "Mengucapkan",
                "This": "Ini",
                "In": "Dalam",
                "English": "Bahasa Inggris"
            }
        },
        {
            "en": "Please speak more slowly.",
            "id": "Tolong berbicaralah lebih pelan.",
            "explanation": {
                "Please": "Tolong",
                "Speak": "Berbicara",
                "More": "Lebih",
                "Slowly": "Pelan"
            }
        },
        {
            "en": "I need help.",
            "id": "Saya butuh bantuan.",
            "explanation": {
                "I": "Saya",
                "Need": "Butuh",
                "Help": "Bantuan"
            }
        },
        {
            "en": "Where can I find a taxi?",
            "id": "Di mana saya bisa menemukan taksi?",
            "explanation": {
                "Where": "Di mana",
                "Can": "Bisa",
                "I": "Saya",
                "Find": "Menemukan",
                "A": "Sebuah",
                "Taxi": "Taksi"
            }
        },
        {
            "en": "How long does it take?",
            "id": "Berapa lama waktu yang dibutuhkan?",
            "explanation": {
                "How": "Berapa",
                "Long": "Lama",
                "Does": "Apakah",
                "It": "Itu",
                "Take": "Dibutuhkan"
            }
        },
        {
            "en": "Can you recommend a restaurant?",
            "id": "Bisakah kamu merekomendasikan restoran?",
            "explanation": {
                "Can": "Bisa",
                "You": "Kamu",
                "Recommend": "Merekomendasikan",
                "A": "Sebuah",
                "Restaurant": "Restoran"
            }
        }
    ]

# Jalankan pembuatan video
if __name__ == "__main__":
    generate_language_learning_video(SENTENCES)



