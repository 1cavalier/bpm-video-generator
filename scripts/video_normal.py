import json
import math
import os

import imageio.v2 as imageio
import numpy as np
from PIL import Image, ImageDraw, ImageFont

JSON_FILE = "../output/heart_rate_data.json"
HEART_FILE = "../assets/coeur.png"
OUTPUT_FILE = "../output/overlay.mp4"

WIDTH = 600
HEIGHT = 200
FPS = 30

with open(JSON_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

def get_color(bpm):
    if bpm >= 160:
        return (255, 43, 43)
    elif bpm >= 140:
        return (255, 159, 26)
    elif bpm >= 120:
        return (255, 214, 10)
    else:
        return (255, 255, 255)

def load_font(size):
    try:
        return ImageFont.truetype("C:/Windows/Fonts/arial.ttf", size)
    except:
        return ImageFont.load_default()

font = load_font(52)

heart_original = Image.open(HEART_FILE).convert("RGBA")

ratio = 110 / heart_original.height
heart_base = heart_original.resize(
    (int(heart_original.width * ratio), 110),
    Image.LANCZOS
)

def make_frame(i):
    t = i / FPS
    sec = min(int(t), len(data) - 1)

    bpm = data[sec]["bpm"]
    color = get_color(bpm)

    img = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 255))
    draw = ImageDraw.Draw(img)

    pulse = 0.5 * (1 + math.sin(2 * math.pi * (bpm / 60) * t))
    scale = 1 + 0.08 * pulse

    heart = heart_base.resize(
        (int(heart_base.width * scale), int(heart_base.height * scale)),
        Image.LANCZOS
    )

    img.alpha_composite(heart, (30, (HEIGHT - heart.height)//2))

    text = f"{bpm} BPM"

    draw.text((182, 70), text, font=font, fill=(0, 0, 0))
    draw.text((180, 68), text, font=font, fill=color)

    return np.array(img.convert("RGB"))

duration = len(data)
total_frames = duration * FPS

os.makedirs("../output", exist_ok=True)

with imageio.get_writer(OUTPUT_FILE, fps=FPS, codec="libx264") as writer:
    for i in range(total_frames):
        if i % FPS == 0:
            print(f"{i//FPS}/{duration} sec")
        writer.append_data(make_frame(i))

print("🎬 Vidéo MP4 créée")