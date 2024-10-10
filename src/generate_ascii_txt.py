import numpy as np
import cv2
import time
from draw_ascii import *
import os
from dotenv import load_dotenv

load_dotenv()
ASCII_LEVEL=int(os.getenv("ASCII_LEVEL"))
ASCII_OUTPUT_WIDTH=int(os.getenv("ASCII_OUTPUT_WIDTH"))
ASCII_OUTPUT_HEIGHT=int(os.getenv("ASCII_OUTPUT_HEIGHT"))
p = Path(__file__).parent.parent
font_p = str(p / "data/ARIAL.TTF")
video_p = str(p / "data/bad-apple.mp4")
out_p = str(p / "bad-apple.txt")

cap = cv2.VideoCapture(video_p)
# fps = cap.get(cv2.CAP_PROP_FPS)
# print(cap.read())

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
fps = 60


ascii_gen = ASCII_generate(font_path=font_p, level=ASCII_LEVEL)
chars = ascii_gen.get_result()

drawer = DrawASCII(ASCII_CHARS=chars, output_size=(ASCII_OUTPUT_WIDTH, ASCII_OUTPUT_HEIGHT))

open(out_p, "w").close()
with open(out_p, "a") as f:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        drawer.load_img(img=frame)
        res = drawer.map_px()

        line = ""
        for l in res:
            line = "".join(l)+"\n"
            f.write(line)