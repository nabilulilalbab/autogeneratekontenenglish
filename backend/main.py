import time
from gtts import gTTS
from moviepy.editor import TextClip, CompositeVideoClip, ImageClip, AudioFileClip, concatenate_videoclips, concatenate_audioclips, vfx
from moviepy.config import change_settings
from moviepy.video.fx.all import speedx
from PIL import Image
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)


key = "q3c5bAJCSDLrS1zehfInYOfckKNcdi8KjXWf0awgxrXpGy7sEBrxBtL4"


# Mengubah konfigurasi MoviePy untuk menggunakan `magick`
# Jangan lupa untuk uncomment setting path di local computer mu
change_settings({
    "IMAGEMAGICK_BINARY": "C:/Program Files/ImageMagick-7.1.1-Q16-HDRI/magick.exe"
    
    # Punya mu di bawah ini!!!
    # "IMAGEMAGICK_BINARY": "/usr/bin/magick"
})

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

# Route untuk generate video di frontend 💻
@app.route('/api/generate-video', methods=['POST'])
def create_video():
    try:
        data = request.get_json()
        sentences = data.get('sentences')
        
        if not sentences:
            return jsonify({'error': 'No sentences provided'}), 400
            
        output_file = f"static/videos/output_{int(time.time())}.mp4"
        
        # Generate video
        video_path = generate_language_learning_video(
            sentences=sentences,
            output_file=output_file
        )
        
        return jsonify({
            'success': True,
            'video_url': f'/api/videos/{os.path.basename(video_path)}'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/videos/<filename>')
def serve_video(filename):
    try:
        return send_file(f"static/videos/{filename}")
    except Exception as e:
        return jsonify({'error': str(e)}), 404

if __name__ == '__main__':
    os.makedirs('static/videos', exist_ok=True)
    app.run(debug=True)
