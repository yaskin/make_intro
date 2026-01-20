from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import ImageSequenceClip, AudioFileClip, CompositeAudioClip
import random
import numpy as np

# ====== НАСТРОЙКИ ======
W, H = 1280, 720
bg = (5, 5, 5)
FONT_PATH = "DejaVuSans-Bold.ttf"  # Положи файл рядом со скриптом

# ====== ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ======
def shake():
    return random.randint(-8, 8), random.randint(-5, 5)

def fit_font(draw, text, max_width, start_size):
    """Автоматически подбирает размер шрифта под ширину экрана"""
    size = start_size
    while size > 20:
        font = ImageFont.truetype(FONT_PATH, size)
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        if text_width <= max_width:
            return font
        size -= 4
    return ImageFont.truetype(FONT_PATH, 20)

def draw_text(draw, pos, text, font, color, stroke=3):
    """Рисуем текст с обводкой"""
    draw.text(
        pos, text,
        font=font,
        fill=color,
        anchor="mm",
        stroke_width=stroke,
        stroke_fill=(0, 0, 0)
    )

# ====== КАДРЫ ======
frames = []

# 1️⃣ ИНСТРУКЦИЯ ДЛЯ ЛОХОВ
for _ in range(24):
    img = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(img)

    font = fit_font(d, "ИНСТРУКЦИЯ ДЛЯ ЛОХОВ", int(W * 0.9), 120)
    x, y = W // 2 + shake()[0], H // 2 + shake()[1]
    draw_text(d, (x, y), "ИНСТРУКЦИЯ ДЛЯ ЛОХОВ", font, (180, 180, 180), stroke=3)

    frames.append(np.array(img))

# 2️⃣ WHITE FLASH
frames.append(np.array(Image.new("RGB", (W, H), (255, 255, 255))))

# 3️⃣ ГЕРОЕВ
for _ in range(28):
    img = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(img)

    font = fit_font(d, "ГЕРОЕВ", int(W * 0.9), 200)
    x, y = W // 2 + shake()[0], H // 2 + shake()[1]
    draw_text(d, (x, y), "ГЕРОЕВ", font, (220, 20, 20), stroke=4)

    frames.append(np.array(img))

# ====== СОЗДАЁМ ВИДЕО ======
clip = ImageSequenceClip(frames, fps=24)

# ====== ДОБАВЛЯЕМ ЗВУК ======
whoosh = AudioFileClip("whoosh.wav").volumex(0.8)  # глитч / whoosh
hit = AudioFileClip("hit.wav").set_start(1.8).volumex(1.2)  # удар на "ГЕРОЕВ"

audio = CompositeAudioClip([whoosh, hit])
clip = clip.set_audio(audio)

# ====== ЭКСПОРТ В MP4 ======
clip.write_videofile(
    "instruction_to_heroes.mp4",
    codec="libx264",
    audio_codec="aac",
    fps=24
)
