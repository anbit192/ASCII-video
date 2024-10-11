# %%
import io
import time
import numpy as np
import cv2
import time
import os
from dotenv import load_dotenv
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import threading
from collections import deque
import pygame
import sys

# %%
class ASCII_generate:
    def __init__(self, font_path, level, canvas_shape=(40, 40)):

        self.canvas = np.zeros(shape=canvas_shape) + 255
        self.font = ImageFont.truetype(font_path, size=10)
        self.printables = [chr(i) for i in range(32, 127)]
        self.level = level
        self.sort_brightness()
        self.generate_chars()

    def sort_brightness(self):
        brightnesses = np.zeros(len(self.printables))
        for i in range(len(self.printables)):
            img = Image.fromarray(self.canvas)
            draw = ImageDraw.Draw(img)
            draw.text(xy=(5, 5), text=self.printables[i], font=self.font)
            brightnesses[i] = np.mean(np.array(img))

        self.brightnesses_dict = dict()
        for i in range(len(brightnesses)):
            self.brightnesses_dict[self.printables[i]] = brightnesses[i]

        self.brightnesses_dict = dict(
            sorted(self.brightnesses_dict.items(), key=lambda item: item[1]))

    def generate_chars(self):
        ratios = [i/self.level for i in range(self.level)]
        quantiles = np.quantile(
            np.unique(list(self.brightnesses_dict.values())), ratios)
        final_chars = []
        for q in quantiles:
            final_chars.append(
                np.abs(list(self.brightnesses_dict.values()) - q).argmin())

        self.final_chars = [list(self.brightnesses_dict.keys())[
            i] for i in final_chars][::-1]

    def get_result(self):
        return self.final_chars


class DrawASCII:
    def __init__(self, ASCII_CHARS, output_size, alpha=1.1, beta=-25):

        self.ASCII_CHARS = ASCII_CHARS
        self.output_size = output_size
        self.alpha = alpha
        self.beta = beta

    def load_img_by_path(self, img_path):
        # if (img_path):
        self.image = cv2.imread(img_path)
        self.image = cv2.resize(self.image, self.output_size)
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        # self.image = cv2.convertScaleAbs(self.image, alpha=self.alpha, beta=self.beta)

    def load_img(self, img):
        self.image = img
        self.image = cv2.resize(self.image, self.output_size)
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        # self.image = cv2.convertScaleAbs(self.image, alpha=self.alpha, beta=self.beta)

    def map_px(self):
        ratio = 255/(len(self.ASCII_CHARS))
        converted = (self.image / ratio).astype(int)
        converted = np.clip(converted, 0, len(self.ASCII_CHARS) - 1)
        return np.array(self.ASCII_CHARS)[converted]

# %%


load_dotenv()
ASCII_LEVEL=int(os.getenv("ASCII_LEVEL"))
ASCII_OUTPUT_WIDTH=int(os.getenv("ASCII_OUTPUT_WIDTH"))
ASCII_OUTPUT_HEIGHT=int(os.getenv("ASCII_OUTPUT_HEIGHT"))
p = Path("../data")
font_p = str(p / "ARIAL.TTF")
video_p = str(p / "bad-apple.mp4")
out_p = str(p / "bad-apple.txt")
music_path = str(p / "bad-apple.mp3")

cap = cv2.VideoCapture(video_p)
# fps = cap.get(cv2.CAP_PROP_FPS)
# print(cap.read())

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
# fps = 60
fps = int(os.getenv("FPS"))
# fps = int(os.getenv())

ascii_gen = ASCII_generate(font_path=font_p, level=ASCII_LEVEL)
chars = ascii_gen.get_result()

drawer = DrawASCII(ASCII_CHARS=chars, output_size=(ASCII_OUTPUT_WIDTH, ASCII_OUTPUT_HEIGHT))

buffer_queue = deque()
BUFFER_SIZE = 128

pygame.mixer.init()
os.system("cls")
pygame.mixer.music.load(music_path)
pygame.mixer.music.set_volume(0.10)

def play_music():
    pygame.mixer.music.play()

def buffer_video(cap, buffer_queue):
    while cap.isOpened():
        if (len(buffer_queue) < BUFFER_SIZE):
            ret, frame = cap.read()
            if not ret:
                break
            drawer.load_img(img=frame)
            res = drawer.map_px()

            buffer_queue.append(res)
        else:
            time.sleep(0.01)

buffer_thread = threading.Thread(target=buffer_video, args=(cap, buffer_queue))
buffer_thread.start()

music_thread = threading.Thread(target=play_music)
music_thread.start()

# count = 0
while buffer_thread.is_alive():
    if (buffer_queue):
        res = buffer_queue.popleft()

        temp = ""
        for l in res:
            temp += "".join(l)+"\n"
        sys.stdout.write("\033[H" + temp)

        time.sleep(1/fps)
        # count += 1

buffer_thread.join()
music_thread.join()

pygame.mixer.music.stop()
cap.release()

