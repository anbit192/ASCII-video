import numpy as np
import time
import os
import cv2
from dotenv import load_dotenv
from pathlib import Path
import threading
from collections import deque
import pygame
import sys
from draw_ascii import *

# New version, generate ASCII and display its frames in real time


load_dotenv()
ASCII_LEVEL=16
ASCII_OUTPUT_WIDTH=275
ASCII_OUTPUT_HEIGHT=82
BUFFER_SIZE = 1024
FPS = 60

exit_flag = threading.Event()


def play_music():
    pygame.mixer.music.play()

def buffer_video(cap, buffer_queue, drawer):
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

def main():
    p = Path(__file__).parent.parent
    music_path = str(p / "data/p5r-reaper.mp3")
    font_p = str(p / "data/ARIAL.TTF")
    video_p = str(p / "data/p5r-reaper.mp4")
    # out_p = str(p / "bad-apple.txt")

    pygame.mixer.init()
    os.system("cls")
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.set_volume(0.3)

    cap = cv2.VideoCapture(video_p)
    # fps = cap.get(cv2.CAP_PROP_FPS)
    # print(cap.read())

    ascii_gen = ASCII_generate(font_path=font_p, level=ASCII_LEVEL)
    chars = ascii_gen.get_result()

    drawer = DrawASCII(ASCII_CHARS=chars, output_size=(ASCII_OUTPUT_WIDTH, ASCII_OUTPUT_HEIGHT))

    buffer_queue = deque()
    os.system("")

    buffer_thread = threading.Thread(target=buffer_video, args=(cap, buffer_queue, drawer))
    buffer_thread.start()

    music_thread = threading.Thread(target=play_music)
    music_thread.start()


    try:
        while (buffer_thread.is_alive() or pygame.mixer.music.get_busy()):
            if (buffer_queue):
                res = buffer_queue.popleft()

                temp = ""
                for l in res:
                    temp += "".join(l)+"\n"
                sys.stdout.write("\033[H" + temp)

                time.sleep(1/FPS)
                # count += 1

    except KeyboardInterrupt:
        print("bye!")
        exit_flag.set()
        
        buffer_thread.join()
        music_thread.join()

    if (music_thread.is_alive() == False):
        pygame.mixer.music.stop()

    cap.release()

if __name__ == "__main__":
    main()
