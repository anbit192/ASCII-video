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
ASCII_LEVEL=int(os.getenv("ASCII_LEVEL"))
ASCII_OUTPUT_WIDTH=int(os.getenv("ASCII_OUTPUT_WIDTH"))
ASCII_OUTPUT_HEIGHT=int(os.getenv("ASCII_OUTPUT_HEIGHT"))
BUFFER_SIZE = 48
FPS = int(os.getenv("FPS"))

exit_flag = threading.Event()


def play_music():
    pygame.mixer.music.play()

# def buffer_video(cap, buffer_queue, drawer):
#     while cap.isOpened():
#         if (len(buffer_queue) < BUFFER_SIZE):
#             ret, frame = cap.read()
#             if not ret:
#                 break
#             drawer.load_img(img=frame)
#             res = drawer.map_px()

#             buffer_queue.append(res)


def main():
    p = Path(__file__).parent.parent
    music_path = str(p / "data/bad-apple.mp3")
    font_p = str(p / "data/ARIAL.TTF")
    video_p = str(p / "data/bad-apple.mp4")
    # out_p = str(p / "bad-apple.txt")

    pygame.mixer.init()
    os.system("cls")
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.set_volume(0.10)

    cap = cv2.VideoCapture(video_p)

    frame_duration = 1/FPS

    ascii_gen = ASCII_generate(font_path=font_p, level=ASCII_LEVEL)
    chars = ascii_gen.get_result()
    # chars[0] = " "
    # chars[1] = "."
    # chars[2] = "/"

    print("Enable color? (0/1)")
    color = int(input())

    drawer = DrawASCII(ASCII_CHARS=chars, output_size=(ASCII_OUTPUT_WIDTH, ASCII_OUTPUT_HEIGHT), color=(1==color))

    music_thread = threading.Thread(target=play_music)
    music_thread.start()

    ulti_start = time.perf_counter()

    while cap.isOpened():
        ret, frame = cap.read()
        start_time = time.time()
        curr = time.perf_counter() - ulti_start
        
        if not ret:
            break
        target_frame = int(curr * FPS)
        actual_frame = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
        if actual_frame < target_frame:
            cap.set(cv2.CAP_PROP_POS_FRAMES, target_frame)
            continue
        drawer.load_img(img=frame)

        res = drawer.get_result()


        temp = "\n".join("".join(line) for line in res)
        sys.stdout.write("\x1B[H" +temp)

        end_time = time.time()

        process_time = end_time - start_time

        if (process_time < frame_duration): # Just in case the frame is slower than the delay
            time.sleep(frame_duration - process_time)

        sys.stdout.write(f"\nExpected Frame: \x1B[32m{target_frame}\x1B[0m, Actual Frame: \x1B[32m{actual_frame}\x1B[0m")

        
    sys.stdout.write("\x1B[0m")

    cap.release()

if __name__ == "__main__":
    main()
